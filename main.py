import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="AgentRouter Setup — Claude Code",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Inject custom CSS to match the glassmorphism and neon aesthetics
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Typography */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: -0.02em;
    }

    /* Background and Theme Variables */
    .stApp {
        background-color: #050505;
        background-image: 
            radial-gradient(circle at 15% 50%, rgba(0, 229, 255, 0.04) 0%, transparent 50%),
            radial-gradient(circle at 85% 30%, rgba(245, 158, 11, 0.04) 0%, transparent 50%);
        background-attachment: fixed;
        color: #F3F4F6;
    }

    /* Hero Section */
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #FFFFFF 0%, #A1A1AA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 16px;
        line-height: 1.2;
    }
    .hero-subtitle {
        color: #9CA3AF;
        font-size: 1.1rem;
        text-align: center;
        margin: 0 auto 32px;
        max-width: 50ch;
    }
    
    /* Sexy Glowing Button */
    .btn-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .hero-btn {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: #FFF !important;
        font-weight: 600;
        padding: 16px 32px;
        border-radius: 12px;
        text-decoration: none;
        font-size: 16px;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
        animation: pulseGlow 3s infinite;
    }
    .hero-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.5);
    }
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.4); }
        70% { box-shadow: 0 0 20px 10px rgba(245, 158, 11, 0); }
        100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }
    }

    /* Credits & Tiny Text */
    .credits { text-align: center; font-size: 15px; color: #9CA3AF; }
    .credits b { color: #F59E0B; text-shadow: 0 0 10px rgba(245, 158, 11, 0.4); font-weight: 600;}
    .tiny { text-align: center; margin-top: 8px; font-size: 12px; color: #6B7280; margin-bottom: 40px;}

    /* Security Warning Note */
    .note-red {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, rgba(239, 68, 68, 0.02) 100%);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-left: 4px solid #EF4444;
        border-radius: 12px;
        padding: 24px;
        font-size: 14px;
        color: #9CA3AF;
        margin-bottom: 30px;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.05);
    }
    .note-red strong {
        color: #EF4444;
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 15px;
        margin-bottom: 8px;
    }

    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 40px 0 16px;
        display: flex;
        align-items: center;
        gap: 12px;
        color: #F3F4F6;
    }
    .section-header span { color: #00E5FF; }
    .lead { color: #9CA3AF; font-size: 15px; margin-bottom: 24px; }

    /* Glassmorphism Steps */
    .step {
        background: rgba(20, 22, 28, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .step:hover {
        background: rgba(30, 33, 40, 0.8);
        border-color: rgba(255, 255, 255, 0.15);
        transform: translateX(4px);
    }
    .step-title {
        display: flex;
        align-items: center;
        gap: 12px;
        font-weight: 600;
        margin-bottom: 8px;
        font-size: 1.1rem;
        color: #F3F4F6;
    }
    .num {
        width: 28px; height: 28px;
        background: rgba(0, 229, 255, 0.1);
        border: 1px solid rgba(0, 229, 255, 0.2);
        border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
        color: #00E5FF;
        flex-shrink: 0;
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.4);
    }
    .step p { margin: 0; color: #9CA3AF; font-size: 15px; }
    
    /* Footer */
    .footer {
        text-align: center;
        padding-top: 40px;
        margin-top: 60px;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
        padding-bottom: 40px;
    }
    .guided-by { font-size: 12px; color: #9CA3AF; opacity: 0.8; }
    .guided-by strong { color: #F3F4F6; font-weight: 600; }
    .footer a {
        display: inline-flex; align-items: center; gap: 6px;
        color: #00E5FF; text-decoration: none; font-size: 12px;
        font-weight: 500; transition: all 0.2s;
        padding: 6px 12px; border-radius: 20px;
        background: rgba(0, 229, 255, 0.05);
        border: 1px solid rgba(0, 229, 255, 0.1);
    }
    .footer a:hover {
        color: #FFF; background: rgba(0, 229, 255, 0.15);
        border-color: rgba(0, 229, 255, 0.3);
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("""
<div class="hero-title">Set up Claude Code <br>with AgentRouter</div>
<div class="hero-subtitle">One API key dynamically routed to Claude and 30+ other models. The ultimate developer setup, from start to finish.</div>
<div class="btn-container">
    <a class="hero-btn" href="https://agentrouter.org/register?aff=7ali" target="_blank" rel="noopener">Claim $50+ Developer Credits →</a>
</div>
<div class="credits"><b>Click to get $50+ free credits</b> and also earn credits by referrals! </div>
<div class="tiny">No credit card required. Instant access via GitHub OAuth.</div>
""", unsafe_allow_html=True)

# --- Security Warning ---
st.markdown("""
<div class="note-red">
    <strong>🚨 Critical Security Warning</strong>
    If you are using this tool, <b>do not share your personal data</b>. Ensure you strictly exclude any sensitive files in your project such as <code>.env</code> files, API keys, and any confidential data related to you or your company. This is a proxy gateway, and you should treat your prompts accordingly.
</div>
""", unsafe_allow_html=True)

# --- Step 1: Create Account ---
st.markdown('<div class="section-header"><span>01.</span> Create your account</div>', unsafe_allow_html=True)

st.markdown("""
<div class="step">
    <div class="step-title"><span class="num">1</span> Have a GitHub account</div>
    <p>Sign-up is GitHub OAuth only — no separate password. Create one at github.com first if you don't have one.</p>
</div>
<div class="step">
    <div class="step-title"><span class="num">2</span> Register via the link above</div>
    <p>Click "Sign in with GitHub" and authorize the app. Your credits land immediately.</p>
</div>
<div class="step">
    <div class="step-title"><span class="num">3</span> Grab your API key</div>
    <p>Go to the token console and generate a key. Copy it now — it's only shown once.</p>
</div>
""", unsafe_allow_html=True)
st.code("https://agentrouter.org/console/token", language="http")

# --- Step 2: Install Claude Code ---
st.markdown('<div class="section-header"><span>02.</span> Install Claude Code</div>', unsafe_allow_html=True)
st.markdown('<div class="lead">Requires Node.js 18 or newer. Select your operating system.</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["macOS", "Linux", "Windows"])

with tab1:
    st.caption("Install Node.js (via Homebrew):")
    st.code("brew install node", language="bash")
    st.caption("Install Claude Code globally:")
    st.code("npm install -g @anthropic-ai/claude-code", language="bash")

with tab2:
    st.caption("Install Node.js (Debian/Ubuntu):")
    st.code("curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -\nsudo apt-get install -y nodejs", language="bash")
    st.caption("Install Claude Code globally:")
    st.code("npm install -g @anthropic-ai/claude-code", language="bash")

with tab3:
    st.caption("Install Node.js via winget:")
    st.code("winget install OpenJS.NodeJS.LTS", language="powershell")
    st.caption("Install Claude Code (PowerShell):")
    st.code("npm install -g @anthropic-ai/claude-code", language="powershell")


# --- Step 3: Environment & Model Setup ---
# Note: Models updated based on requested reference to image_84848d.png verbatim
st.markdown('<div class="section-header"><span>03.</span> Environment & Model Setup</div>', unsafe_allow_html=True)
st.markdown('<div class="lead">Route Claude Code to AgentRouter and choose one of the available models.</div>', unsafe_allow_html=True)

env_tab1, env_tab2, env_tab3 = st.tabs(["macOS", "Linux", "Windows"])

with env_tab1:
    st.caption("Add to `~/.zshrc` (or `~/.bash_profile`):")
    st.code("""export ANTHROPIC_BASE_URL="https://agentrouter.org/"
export ANTHROPIC_AUTH_TOKEN="sk-your-agentrouter-key-here"
export ANTHROPIC_API_KEY="sk-your-agentrouter-key-here"

# Choose your model (Available: claude-opus-4-8, claude-opus-5, gpt-5.6-sol)
export ANTHROPIC_MODEL="claude-opus-5" """, language="bash")
    st.caption("Reload your shell:")
    st.code("source ~/.zshrc", language="bash")

with env_tab2:
    st.caption("Add to `~/.bashrc`:")
    st.code("""export ANTHROPIC_BASE_URL="https://agentrouter.org/"
export ANTHROPIC_AUTH_TOKEN="sk-your-agentrouter-key-here"
export ANTHROPIC_API_KEY="sk-your-agentrouter-key-here"

# Choose your model (Available: claude-opus-4-8, claude-opus-5, gpt-5.6-sol)
export ANTHROPIC_MODEL="claude-opus-5" """, language="bash")
    st.caption("Reload your shell:")
    st.code("source ~/.bashrc", language="bash")

with env_tab3:
    st.caption("In PowerShell, add to your profile (`$PROFILE`):")
    st.code("""$env:ANTHROPIC_BASE_URL = "https://agentrouter.org/"
$env:ANTHROPIC_AUTH_TOKEN = "sk-your-agentrouter-key-here"
$env:ANTHROPIC_API_KEY = "sk-your-agentrouter-key-here"

# Choose your model (Available: claude-opus-4-8, claude-opus-5, gpt-5.6-sol)
$env:ANTHROPIC_MODEL = "claude-opus-5" """, language="powershell")
    st.caption("Or set them permanently at the system level:")
    st.code("""setx ANTHROPIC_BASE_URL "https://agentrouter.org/"
setx ANTHROPIC_AUTH_TOKEN "sk-your-agentrouter-key-here"
setx ANTHROPIC_API_KEY "sk-your-agentrouter-key-here"
setx ANTHROPIC_MODEL "claude-opus-5" """, language="powershell")
    st.caption("Restart your terminal after using `setx`.")


# --- Step 4: Launch & Verify ---
st.markdown('<div class="section-header"><span>04.</span> Launch & Verify</div>', unsafe_allow_html=True)
st.markdown('<div class="lead">Fire up the CLI to confirm everything is wired correctly.</div>', unsafe_allow_html=True)
st.code("claude", language="bash")
st.caption("Once inside, test its context awareness:")
st.code("> What files are in this directory?", language="plaintext")


# --- Step 5: Available Models ---
st.markdown('<div class="section-header"><span>05.</span> Available Models</div>', unsafe_allow_html=True)

# Updated models based exactly on image_84848d.png
models_data = {
    "Model String": ["claude-opus-5", "claude-opus-4-8", "gpt-5.6-sol"],
    "Best Used For": [
        "Next-generation Anthropic model for everyday coding, tool use & agentic tasks",
        "Legacy powerhouse for deep reasoning and complex architecture",
        "OpenAI's latest specialized model for rapid refactoring and problem solving"
    ]
}

df_models = pd.DataFrame(models_data)
# Applying Streamlit's native dataframe styling for a modern table view
st.dataframe(df_models, hide_index=True, use_container_width=True)


# --- Footer ---
st.markdown("""
<div class="footer">
    <div class="guided-by">
        Guided by <strong>Dipanshu Garg</strong>
    </div>
    <a href="https://www.linkedin.com/in/dipanshu-garg24" target="_blank" rel="noopener">
        <svg style="width:14px; height:14px; fill:currentColor" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
        Follow on LinkedIn
    </a>
</div>
""", unsafe_allow_html=True)
