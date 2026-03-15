# learning

Self-learning agent system for adaptive, privacy-first personalization.

## Structure
- `core/learning_engine.py`: orchestrates interaction capture, feedback processing, preference updates, and local persistence.
- `core/feedback_collector.py`: explicit/implicit feedback and interaction event collection.
- `analysis/behavior_analyzer.py`: derives interests, frequent workflows, and task success patterns.
- `analysis/pattern_detector.py`: lower-level pattern extraction helpers.
- `models/preference_model.py`: long-term user preference profiles.
- `models/policy_model.py`: reinforcement policy scores used to prioritize future decisions.
- `training/reinforcement_trainer.py`: policy updates from reward signals.
- `training/reward_system.py`: reward computation from outcomes and feedback.

## Privacy-first controls
- Local storage by default (`learning/local_learning_data.json`).
- Tracking can be disabled via `LearningEngine.set_tracking_enabled(False)`.
- User learning profile can be reset via `LearningEngine.reset_user_learning_data(user_id)`.
