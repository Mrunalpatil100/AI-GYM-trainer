
import { useState } from "react";
import {
  Dumbbell, Home, Database, BrainCircuit, Camera,
  Info, Play, Activity, Clock, Target, CheckCircle2,
  AlertTriangle, Zap, Menu, RotateCcw
} from "lucide-react";
import "./App.css";

const pages = [
  { name: "Home", icon: Home },
  { name: "Dataset", icon: Database },
  { name: "Train Model", icon: BrainCircuit },
  { name: "Live Trainer", icon: Camera },
  { name: "Model Info", icon: Info },
];

function App() {
  const [page, setPage] = useState("Home");
  const [reps, setReps] = useState(0);
  const [workoutStarted, setWorkoutStarted] = useState(false);
  const [split, setSplit] = useState(20);
  const [algorithm, setAlgorithm] = useState("Random Forest");

  const navigate = (name) => {
    setPage(name);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <div className="app">
      <header className="navbar">
        <button className="brand" onClick={() => navigate("Home")}>
          <span className="brand-icon">🏋️</span>
          <span>AI Gym Trainer</span>
        </button>

        <nav>
          {pages.map(({ name, icon: Icon }) => (
            <button
              key={name}
              className={`nav-link ${page === name ? "active" : ""}`}
              onClick={() => navigate(name)}
            >
              <Icon size={16} />
              {name}
            </button>
          ))}
        </nav>
      </header>

      <main className="main">
        {page === "Home" && (
          <>
            <section className="hero">
              <div className="pill"><Zap size={15} /> POWERED BY MACHINE LEARNING</div>
              <h1>AI Gym <span>Trainer</span></h1>
              <p>
                Real-time exercise form detection, repetition counting,
                and intelligent feedback powered by machine learning.
              </p>
              <div className="hero-actions">
                <button className="primary-btn" onClick={() => navigate("Live Trainer")}>
                  <Play size={17} /> Start Training
                </button>
                <button className="secondary-btn" onClick={() => navigate("Dataset")}>
                  <Database size={17} /> View Dataset
                </button>
              </div>
            </section>

            <section className="how-section">
              <h2>How It Works</h2>
              <p>Your workout passes through three intelligent stages.</p>
              <div className="grid three">
                <InfoCard icon={<Camera />} title="Pose Detection"
                  text="MediaPipe identifies body landmarks from the webcam." />
                <InfoCard icon={<BrainCircuit />} title="ML Prediction"
                  text="Your trained Random Forest model predicts squat form." />
                <InfoCard icon={<Activity />} title="Workout Tracking"
                  text="Track repetitions, session duration and saved history." />
              </div>
            </section>
          </>
        )}

        {page === "Dataset" && (
          <PageHeading
            icon={<Database />}
            title="Exercise Dataset Hub"
            subtitle="Inspect your squat dataset and its training labels."
          >
            <div className="grid four">
              <Metric title="Dataset" value="19,373" caption="Recorded samples" />
              <Metric title="Input Features" value="42" caption="Landmark coordinates" />
              <Metric title="Target Classes" value="2" caption="Correct / Incorrect" />
              <Metric title="Missing Labels" value="0" caption="Reported in dataset inspection" />
            </div>

            <section className="panel">
              <h3>Squat Form Class Distribution</h3>
              <p className="muted">Actual labels from your training CSV.</p>
              <div className="distribution">
                <div>
                  <div className="dist-label"><span className="green">Correct</span><b>13,619</b></div>
                  <div className="bar"><span style={{ width: "70.3%" }} /></div>
                  <small>70.3% of samples</small>
                </div>
                <div>
                  <div className="dist-label"><span className="red">Incorrect</span><b>5,754</b></div>
                  <div className="bar redbar"><span style={{ width: "29.7%" }} /></div>
                  <small>29.7% of samples</small>
                </div>
              </div>
              <p className="note">These values reflect the CSV previously inspected. The dashboard is not yet reading the file directly.</p>
            </section>
          </PageHeading>
        )}

        {page === "Train Model" && (
          <PageHeading
            icon={<BrainCircuit />}
            title="Custom ML Model Training & Benchmarking"
            subtitle="Configure a training run and review your existing model."
          >
            <section className="panel">
              <h3><Zap size={19} /> Training Configuration</h3>
              <div className="config-grid">
                <label>
                  Algorithm Selection
                  <select value={algorithm} onChange={e => setAlgorithm(e.target.value)}>
                    <option>Random Forest</option>
                    <option>Logistic Regression</option>
                    <option>Decision Tree</option>
                  </select>
                </label>
                <label>
                  Test Split Ratio: {split}%
                  <input type="range" min="10" max="40" step="5"
                    value={split} onChange={e => setSplit(Number(e.target.value))} />
                </label>
                <button className="primary-btn" onClick={() => alert(
                  "This button is a frontend preview. We will connect it to the Python training script next."
                )}>
                  <Zap size={17} /> Train ML Model
                </button>
              </div>
            </section>
            <div className="grid four">
              <Metric title="Saved Model" value="Random Forest" caption="Current classifier" />
              <Metric title="Test Accuracy" value="99.46%" caption="Previous random-split evaluation" />
              <Metric title="Input Features" value="42" caption="Landmark coordinates" />
              <Metric title="Test Split" value={`${split}%`} caption="Selected configuration only" />
            </div>
            <section className="panel">
              <h3>Training status</h3>
              <p className="muted">
                Current model: squat_model.pkl. Training settings on this page are visual controls;
                they do not retrain the model yet.
              </p>
            </section>
          </PageHeading>
        )}

        {page === "Live Trainer" && (
          <PageHeading
            icon={<Camera />}
            title="Live AI Gym Trainer"
            subtitle="Real-time pose analysis, squat form prediction and repetition tracking."
          >
            <div className="live-actions">
              <button className="secondary-btn" onClick={() => setReps(0)}>
                <RotateCcw size={16} /> Reset Reps
              </button>
              <button className="primary-btn"
                onClick={() => setWorkoutStarted(!workoutStarted)}>
                <Play size={16} /> {workoutStarted ? "Stop Preview" : "Start Workout"}
              </button>
            </div>
            <div className="grid five">
              <Metric title="TOTAL REPS" value={reps} caption="This session" />
              <Metric title="PERFECT FORM" value="—" caption="Connect model first" />
              <Metric title="MISTAKES" value="—" caption="Connect model first" />
              <Metric title="FORM ACCURACY" value="—" caption="Not yet calculated" />
              <Metric title="PHASE" value={workoutStarted ? "READY" : "STANDING"} caption="Preview state" />
            </div>
            <div className="live-grid">
              <section className="camera-panel">
                <div className="camera-placeholder">
                  <div className="camera-symbol"><Camera size={48} /></div>
                  <h3>{workoutStarted ? "Camera integration pending" : "Live camera preview"}</h3>
                  <p>
                    {workoutStarted
                      ? "Tomorrow, connect your webcam and Python pose-detection pipeline here."
                      : "Start the preview to see the integration status."}
                  </p>
                  <span className="pill">WEBCAM NOT CONNECTED TO WEBSITE</span>
                </div>
              </section>
              <div className="stack">
                <section className="panel">
                  <h3><Activity size={18} /> Biomechanical Angles</h3>
                  <div className="angle-row"><span>Knee angle</span><b>—</b></div>
                  <div className="angle-row"><span>Torso lean</span><b>—</b></div>
                  <div className="angle-row"><span>Stance symmetry</span><b>—</b></div>
                  <p className="note">Live measurements will appear after integration.</p>
                </section>
                <section className="panel">
                  <h3><BrainCircuit size={18} /> Active ML Model</h3>
                  <p className="detail"><b>Architecture:</b> MediaPipe + Scikit-learn</p>
                  <p className="detail"><b>Classifier:</b> Random Forest</p>
                  <p className="detail"><b>Input features:</b> 42 landmarks</p>
                  <p className="detail"><b>Status:</b> UI preview only</p>
                </section>
              </div>
            </div>
          </PageHeading>
        )}

        {page === "Model Info" && (
          <PageHeading
            icon={<Info />}
            title="Model Information"
            subtitle="Understand the model powering your squat classifier."
          >
            <div className="grid three">
              <Metric title="Algorithm" value="Random Forest" caption="Ensemble classifier" />
              <Metric title="Input Dimensions" value="42" caption="14 landmarks × 3 coordinates" />
              <Metric title="Model File" value="squat_model.pkl" caption="Saved Python model" />
            </div>
            <section className="panel">
              <h3><CheckCircle2 size={19} /> Model Pipeline</h3>
              {["Capture body landmarks with MediaPipe",
                "Convert 14 landmarks into 42 coordinate features",
                "Pass the features to the saved Random Forest",
                "Display the correct/incorrect frame prediction"
              ].map((item, i) => (
                <div className="pipeline-row" key={item}>
                  <span className="step-number">{i + 1}</span><span>{item}</span>
                </div>
              ))}
            </section>
            <section className="panel">
              <h3><AlertTriangle size={19} /> Evaluation note</h3>
              <p className="muted">
                The previously measured 99.46% score came from a random frame-level split.
                Similar frames may occur in both sets, so it should not be treated as proven
                real-world accuracy. A grouped evaluation is a useful next improvement.
              </p>
            </section>
          </PageHeading>
        )}
      </main>

      <footer>AI Gym Trainer · Machine Learning Project · React + Vite</footer>
    </div>
  );
}

function PageHeading({ icon, title, subtitle, children }) {
  return (
    <section className="content-page">
      <div className="page-heading">
        <div className="page-icon">{icon}</div>
        <div><h1>{title}</h1><p>{subtitle}</p></div>
      </div>
      {children}
    </section>
  );
}

function Metric({ title, value, caption }) {
  return (
    <div className="metric">
      <span className="metric-title">{title}</span>
      <strong>{value}</strong>
      <small>{caption}</small>
    </div>
  );
}

function InfoCard({ icon, title, text }) {
  return (
    <div className="info-card">
      <div className="info-icon">{icon}</div>
      <h3>{title}</h3>
      <p>{text}</p>
    </div>
  );
}

export default App;
