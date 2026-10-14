// ============================================================
// GYM MANAGEMENT SYSTEM - MONGODB SETUP SCRIPT
// Database: MongoDB 7.x
// ============================================================

use("gym_db");

// Drop existing collections if they exist (clean slate)
db.workout_plans.drop();
db.feedback.drop();
db.presets.drop();

// ============================================================
// COLLECTION 1: workout_plans (10 members)
// ============================================================

db.workout_plans.insertMany([
  {
    member_id: 1,
    trainer_id: 1,
    goal: "Weight Loss",
    plan: [
      { day: "Mon", exercises: ["Treadmill 20min", "Squats 3x12"] },
      { day: "Wed", exercises: ["Cycling 30min", "Pushups 3x15"] },
      { day: "Fri", exercises: ["Rowing 15min", "Lunges 3x12"] }
    ],
    created_at: "2026-01-12"
  },
  {
    member_id: 2,
    trainer_id: 2,
    goal: "General Fitness",
    plan: [
      { day: "Tue", exercises: ["Jogging 30min", "Yoga 20min"] },
      { day: "Thu", exercises: ["Stretching 15min", "Plank 3x60s"] },
      { day: "Sat", exercises: ["Cycling 25min"] }
    ],
    created_at: "2026-02-17"
  },
  {
    member_id: 3,
    trainer_id: 3,
    goal: "Muscle Gain",
    plan: [
      { day: "Mon", exercises: ["Bench Press 4x8", "Deadlift 3x6"] },
      { day: "Wed", exercises: ["Pull-ups 3x10", "Rows 3x12"] },
      { day: "Fri", exercises: ["Overhead Press 3x10", "Curls 3x12"] }
    ],
    created_at: "2026-03-03"
  },
  {
    member_id: 4,
    trainer_id: 4,
    goal: "Strength Training",
    plan: [
      { day: "Tue", exercises: ["Barbell Squats 4x6", "Bench Press 4x6"] },
      { day: "Thu", exercises: ["Deadlift 3x5", "Plank 3x60s"] },
      { day: "Sat", exercises: ["Power Cleans 3x5"] }
    ],
    created_at: "2026-03-22"
  },
  {
    member_id: 5,
    trainer_id: 5,
    goal: "Endurance",
    plan: [
      { day: "Mon", exercises: ["Running 40min", "Jump Rope 10min"] },
      { day: "Wed", exercises: ["Rowing 20min", "Cycling 30min"] },
      { day: "Fri", exercises: ["Swimming 30min"] }
    ],
    created_at: "2026-04-07"
  },
  {
    member_id: 6,
    trainer_id: 1,
    goal: "Weight Loss",
    plan: [
      { day: "Tue", exercises: ["Treadmill 25min", "Burpees 3x15"] },
      { day: "Thu", exercises: ["Cycling 30min", "Mountain Climbers 3x20"] },
      { day: "Sat", exercises: ["HIIT 20min"] }
    ],
    created_at: "2026-04-20"
  },
  {
    member_id: 7,
    trainer_id: 2,
    goal: "Muscle Gain",
    plan: [
      { day: "Mon", exercises: ["Squats 4x8", "Deadlift 4x6"] },
      { day: "Wed", exercises: ["Bench Press 4x8", "Pull-ups 3x10"] },
      { day: "Fri", exercises: ["Overhead Press 3x10", "Barbell Rows 3x12"] }
    ],
    created_at: "2026-05-04"
  },
  {
    member_id: 8,
    trainer_id: 4,
    goal: "General Fitness",
    plan: [
      { day: "Tue", exercises: ["Yoga 45min", "Stretching 15min"] },
      { day: "Thu", exercises: ["Jogging 30min"] },
      { day: "Sat", exercises: ["Cycling 40min"] }
    ],
    created_at: "2026-05-17"
  },
  {
    member_id: 9,
    trainer_id: 3,
    goal: "Endurance",
    plan: [
      { day: "Mon", exercises: ["Cycling 45min", "Core Work 10min"] },
      { day: "Wed", exercises: ["Running 30min"] },
      { day: "Fri", exercises: ["Rowing 25min"] }
    ],
    created_at: "2026-06-03"
  },
  {
    member_id: 10,
    trainer_id: 5,
    goal: "Muscle Gain",
    plan: [
      { day: "Tue", exercises: ["Bench Press 3x8", "Dumbbell Rows 3x10"] },
      { day: "Thu", exercises: ["Squats 3x10", "Curls 3x12"] },
      { day: "Sat", exercises: ["Shoulder Press 3x10"] }
    ],
    created_at: "2026-06-22"
  }
]);

// ============================================================
// COLLECTION 2: feedback (10 entries)
// ============================================================

db.feedback.insertMany([
  { member_id: 1, rating: 5, comments: "Great trainers, clean equipment. Worth every rupee!", date: "2026-08-15" },
  { member_id: 2, rating: 4, comments: "Good ambiance, equipment could be newer", date: "2026-08-22" },
  { member_id: 3, rating: 5, comments: "Lost 8 kgs in 3 months. Trainers really know their stuff.", date: "2026-08-30" },
  { member_id: 4, rating: 5, comments: "CrossFit sessions are intense but effective", date: "2026-09-05" },
  { member_id: 5, rating: 4, comments: "Zumba class is fun. Would love more slots.", date: "2026-09-10" },
  { member_id: 6, rating: 5, comments: "Best gym in the area. Highly recommend!", date: "2026-09-15" },
  { member_id: 7, rating: 3, comments: "Good workouts but peak hours get crowded", date: "2026-09-20" },
  { member_id: 8, rating: 5, comments: "Yoga sessions are amazing. Very peaceful environment.", date: "2026-09-25" },
  { member_id: 9, rating: 4, comments: "Great place, reasonable pricing", date: "2026-09-30" },
  { member_id: 10, rating: 5, comments: "Trainer Rahul is the best. Focused and patient.", date: "2026-10-05" }
]);

// ============================================================
// COLLECTION 3: presets
// ============================================================

db.presets.insertMany([
  {
    goal: "Weight Loss",
    exercises: ["Treadmill 20min", "Cycling 30min", "Squats 3x12", "Lunges 3x12"],
    difficulty: "Beginner"
  },
  {
    goal: "Muscle Gain",
    exercises: ["Bench Press 4x8", "Deadlift 3x6", "Pull-ups 3x10", "Overhead Press 3x10"],
    difficulty: "Intermediate"
  },
  {
    goal: "General Fitness",
    exercises: ["Jogging 30min", "Yoga 45min", "Stretching 10min"],
    difficulty: "Beginner"
  },
  {
    goal: "Strength Training",
    exercises: ["Barbell Squats 4x6", "Bench Press 4x6", "Deadlift 3x5", "Plank 3x60s"],
    difficulty: "Advanced"
  },
  {
    goal: "Endurance",
    exercises: ["Running 40min", "Rowing 20min", "Cycling 30min", "Jump Rope 10min"],
    difficulty: "Intermediate"
  }
]);

// ============================================================
// INDEXES
// ============================================================

db.presets.createIndex({ goal: 1 }, { name: "idx_preset_goal" });
db.feedback.createIndex({ date: -1 });
db.workout_plans.createIndex({ created_at: -1 });
db.feedback.createIndex({ member_id: 1 });
db.workout_plans.createIndex({ member_id: 1 });

// ============================================================
// VERIFICATION
// ============================================================

print("=== Average Rating ===");
printjson(db.feedback.aggregate([
  { $group: { _id: null, avgRating: { $avg: "$rating" }, total: { $sum: 1 } } }
]).toArray());

print("=== Counts ===");
print("workout_plans:", db.workout_plans.countDocuments());
print("feedback:", db.feedback.countDocuments());
print("presets:", db.presets.countDocuments());