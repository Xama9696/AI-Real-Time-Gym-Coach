import streamlit as st
import os
import time
import pandas as pd
from services.auth.login_wall import render_login_wall
from services.state.sessions_defaults import initial_session_defaults
from services.config.workout_config import EXERCISE_OPTIONS
from services.ui.style_loader import load_css, inject_local_font, inject_webrtc_styles
from services.persistence.exercise_repository import init_db, get_users_exercises
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from services.vision.exercise_video_processor import VideoProcessorClass
from services.tracking.metrics import sync_metrics_update
from groq import Groq
from services.coaching.llm import LLMCoach
from services.coaching.tts import TextToSpeech
from services.coaching.voice_pipeline import VoicePipeline, autoplay_audio
 
 
def _fire_voice_event(event, exercise, metrics={}):
    """Safely call voice pipeline and store result in session state."""
    try:
        vp = st.session_state.get("voice_pipeline")
        if not vp:
            return
        result = vp.process_event(event=event, exercise=exercise, metrics=metrics)
        if result:
            audio, text = result
            st.session_state.audio_to_play = audio
            st.session_state.coach_feedback = text
            st.session_state.audio_just_played = True
    except Exception:
        pass
 
 
def main():
    st.set_page_config(
        page_icon="🏋️‍♀️",
        page_title="AI Real-time GYM Coach",
        initial_sidebar_state="expanded",
        layout="centered"
    )
 
    load_css(os.path.join(os.getcwd(), "static", "style.css"))
    inject_local_font(os.path.join(os.getcwd(), "static", "AdobeClean.otf"), "AdobeClean")
 
    init_db()
 
    if not render_login_wall():
        return
 
    initial_session_defaults()
 
    if "voice_pipeline" not in st.session_state:
        try:
            api_key = os.environ.get("GROQ_API_KEY", "")
            if not api_key and hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
                api_key = st.secrets["GROQ_API_KEY"]
            groq_client = Groq(api_key=api_key)
            llm_coach = LLMCoach(groq_client)
            tts = TextToSpeech()
            st.session_state.voice_pipeline = VoicePipeline(llm_coach, tts)
        except Exception:
            st.session_state.voice_pipeline = None
 
    workout_started = st.session_state.get("workout_started", False)
 
    with st.sidebar:
        st.title("🏋️‍♂️ Apna AI Coach")
 
        if st.session_state.get("username"):
            st.caption(f"👤 Logged in as {st.session_state.username}")
 
        st.divider()
        st.subheader("Workout Plan")
 
        if not workout_started:
            plan_exercise = st.selectbox("Exercise", options=EXERCISE_OPTIONS, key="plan_exercise")
            plan_sets = st.number_input("Sets", min_value=0, max_value=50, key="plan_sets", step=1)
            plan_reps = st.number_input("Reps per Set", min_value=0, max_value=50, key="plan_reps", step=1)
 
            st.markdown("")
 
            if st.button("Start Workout", use_container_width=True, key="start_session_button"):
                st.session_state.exercise_type = plan_exercise
                st.session_state.target_sets = int(plan_sets)
                st.session_state.reps_per_set = int(plan_reps)
                st.session_state.reps = 0
                st.session_state.workout_started = True
                st.session_state.set_cycle_started_at = time.time()
                st.session_state.last_saved_sets_completed = 0
                st.session_state.last_notified_sets_completed = 0
                st.session_state.last_notified_workout_complete = False
                _fire_voice_event("workout_started", plan_exercise)
                st.rerun()
        else:
            exercise = st.session_state.get("exercise_type")
            sets = st.session_state.get("target_sets")
            reps = st.session_state.get("reps_per_set")
 
            st.info(f"**{exercise}** -- {sets} Sets / {reps} Reps")
 
            if st.button("End Workout", use_container_width=True, key="end_session_button"):
                st.session_state.workout_started = False
                _fire_voice_event("workout_completed", exercise)
                st.rerun()
 
        if workout_started:
            st.divider()
 
            exercise = st.session_state.get("exercise_type")
            total_reps = st.session_state.get("reps")
            current_set_reps = st.session_state.get("current_set_reps")
            reps_per_set = st.session_state.get("reps_per_set")
            sets_completed = st.session_state.get("sets_completed")
            target_sets = st.session_state.get("target_sets")
 
            st.subheader("Progress")
            st.metric("Total Reps", f"{total_reps}")
            st.metric("Current Set Reps", f"{current_set_reps} / {reps_per_set}")
            st.metric("Sets Completed", f"{sets_completed} / {target_sets}")
 
            st.divider()
 
            if exercise == "Squats":
                st.subheader("Squat Metrics")
                st.metric("Knee Angle", f"{st.session_state.get('knee_angle', '--')}°")
                st.metric("Back Angle", f"{st.session_state.get('back_angle', '--')}°")
                st.metric("Depth Status", st.session_state.get("depth_status", "--"))
 
            elif exercise == "Push-ups":
                st.subheader("Push-up Metrics")
                st.metric("Elbow Angle", f"{st.session_state.get('elbow_angle', '--')}°")
                st.metric("Body Alignment", st.session_state.get("body_alignment", "--"))
                st.metric("Hip Position", st.session_state.get("hip_status", "--"))
 
            elif exercise == "Biceps Curls (Dumbbell)":
                st.subheader("Curl Metrics")
                st.metric("Elbow Angle", f"{st.session_state.get('elbow_angle', '--')}°")
                st.metric("Shoulder Stability", st.session_state.get("shoulder_status", "--"))
                st.metric("Swing Detection", st.session_state.get("swing_status", "--"))
 
            elif exercise == "Shoulder Press":
                st.subheader("Shoulder Press Metrics")
                st.metric("Elbow Angle", f"{st.session_state.get('elbow_angle', '--')}°")
                st.metric("Arm Extension", st.session_state.get("extension_status", "--"))
                st.metric("Back Arch", st.session_state.get("back_arch_status", "--"))
 
            elif exercise == "Lunges":
                st.subheader("Lunge Metrics")
                st.metric("Front Knee Angle", f"{st.session_state.get('front_knee_angle', '--')}°")
                st.metric("Torso Angle", f"{st.session_state.get('torso_angle', '--')}°")
                st.metric("Balance Status", st.session_state.get("balance_status", "--"))
 
    st.title("AI Real-time GYM Coach")
    st.markdown("#### Real-time pose detection with proactive AI voice coaching")
 
    if st.session_state.get("audio_to_play"):
        autoplay_audio(st.session_state.audio_to_play)
        st.session_state.audio_to_play = None
 
    if st.session_state.get("coach_feedback"):
        st.markdown("")
        st.success(f"🤖 **Coach:** {st.session_state.coach_feedback}")
 
    if not workout_started:
        st.markdown(
            """
            <div style="
                border: 10px dashed #444;
                border-radius: 0px;
                padding: 48px 32px;
                text-align: center;
                color: #888;
                margin-top: 32px;
                margin-bottom: 32px;
            ">
                <h2 style="color:#ccc; margin-bottom:8px;">👈 Set your workout plan</h2>
                <p style="font-size:1.05rem;">
                    Choose your exercise, sets and reps in the sidebar,<br>
                    then click <strong>Start Workout</strong> to activate the camera and AI coach.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        context = webrtc_streamer(
            key="exercise-analysis",
            mode=WebRtcMode.SENDRECV,
            video_processor_factory=VideoProcessorClass,
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            media_stream_constraints={"video": True, "audio": False},
            async_processing=True,
        )
 
        inject_webrtc_styles()
        sync_metrics_update(context)
 
        if context.state.playing:
            time.sleep(0.25)
            st.rerun()
 
    st.divider()
    st.markdown("#### Workout History")
 
    user_id = st.session_state.get("user_id")
 
    if user_id is not None:
        history_rows = get_users_exercises(user_id)
 
        arr = [
            {
                "Exercise": row["exercise_name"],
                "Reps": row["reps"],
                "Sets": row["sets"],
                "Time (sec)": row["time"],
                "Date": row["created_at"],
            }
            for row in history_rows
        ]
 
        df = pd.DataFrame(arr)
 
        if not df.empty:
            df["Date"] = pd.to_datetime(df["Date"]).dt.date
            agg_df = (
                df.groupby(["Exercise", "Date"])
                .agg({"Reps": "sum", "Sets": "sum", "Time (sec)": "sum"})
                .reset_index()
            )
            agg_df.index += 1
            st.table(agg_df)
        else:
            st.info("No workout history found.")
    else:
        st.info("No workout history found.")
 
 
main()