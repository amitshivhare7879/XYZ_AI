/**
 * XYZ AI — Shared 3D & Viseme Avatar Controller (shared/avatar.js)
 * Provides unified, high-performance avatar rendering with phoneme viseme lip-sync,
 * eye blinking, breathing animations, and role-specific persona styling.
 */

(function(global) {
  class SchoolAvatarController {
    constructor(options = {}) {
      this.canvas = typeof options.canvas === 'string' ? document.getElementById(options.canvas) : options.canvas;
      this.role = options.role || 'student';
      this.avatarUrl = options.avatarUrl || null;
      this.onStateChange = options.onStateChange || null;

      this.ctx = this.canvas ? this.canvas.getContext('2d') : null;
      this.state = 'idle'; // 'idle', 'listening', 'thinking', 'speaking'
      
      // Avatar dynamic parameters
      this.mouthOpen = 0.05;
      this.mouthOpenTarget = 0.05;
      this.mouthWidth = 1.0;
      this.mouthWidthTarget = 1.0;
      this.blinkProgress = 0.0;
      this.eyeGazeX = 0;
      this.eyeGazeY = 0;
      this.headTilt = 0;
      this.headTiltTarget = 0;
      
      this.time = 0;
      this.isSpeaking = false;
      this.visemeInterval = null;
      this.blinkTimer = null;
      this.animationFrame = null;

      // Color Palette by Persona
      this.palettes = {
        student: {
          aura: '#06b6d4',
          accent: '#3b82f6',
          bgStart: '#0f172a',
          bgEnd: '#1e293b',
          tie: '#06b6d4',
          badge: 'STUDENT AI'
        },
        parent: {
          aura: '#8b5cf6',
          accent: '#6366f1',
          bgStart: '#1e1b4b',
          bgEnd: '#312e81',
          tie: '#a855f7',
          badge: 'PARENT SUPPORT'
        },
        teacher: {
          aura: '#10b981',
          accent: '#0d9488',
          bgStart: '#064e3b',
          bgEnd: '#042f2e',
          tie: '#14b8a6',
          badge: 'FACULTY ASST'
        },
        principal: {
          aura: '#f59e0b',
          accent: '#d97706',
          bgStart: '#451a03',
          bgEnd: '#78350f',
          tie: '#f59e0b',
          badge: 'LEADERSHIP AI'
        }
      };

      if (this.canvas) {
        this.initCanvas();
        this.startAnimationLoop();
        this.scheduleBlinks();
      }
    }

    initCanvas() {
      if (!this.canvas) return;
      const dpr = window.devicePixelRatio || 1;
      const rect = this.canvas.getBoundingClientRect();
      const w = rect.width || 320;
      const h = rect.height || 360;
      
      this.canvas.width = w * dpr;
      this.canvas.height = h * dpr;
      this.ctx.scale(dpr, dpr);
      this.width = w;
      this.height = h;
    }

    setState(newState) {
      this.state = newState;
      if (newState === 'speaking') {
        this.isSpeaking = true;
      } else {
        this.isSpeaking = false;
        this.mouthOpenTarget = 0.05;
        this.mouthWidthTarget = 1.0;
      }
      if (this.onStateChange) this.onStateChange(newState);
    }

    scheduleBlinks() {
      const nextBlink = Math.random() * 3000 + 2000;
      this.blinkTimer = setTimeout(() => {
        this.triggerBlink();
        this.scheduleBlinks();
      }, nextBlink);
    }

    triggerBlink() {
      let phase = 0;
      const interval = setInterval(() => {
        phase += 0.2;
        if (phase <= 1) {
          this.blinkProgress = Math.sin(phase * Math.PI);
        } else {
          this.blinkProgress = 0;
          clearInterval(interval);
        }
      }, 25);
    }

    speak(text, onComplete) {
      this.setState('speaking');
      
      // Real-time dynamic phoneme modulation during speech
      clearInterval(this.visemeInterval);
      const visemes = [0.8, 0.25, 0.9, 0.4, 0.7, 0.2, 0.85, 0.5];
      let vIndex = 0;

      this.visemeInterval = setInterval(() => {
        if (this.state === 'speaking') {
          this.mouthOpenTarget = visemes[vIndex % visemes.length];
          this.mouthWidthTarget = 0.9 + (Math.sin(vIndex * 1.5) * 0.25);
          this.headTiltTarget = Math.sin(vIndex * 0.5) * 0.04;
          vIndex++;
        }
      }, 90);

      const cleanVoiceText = text.replace(/\*\*/g, '').replace(/•/g, '').replace(/#/g, '').replace(/₹/g, 'Rupees ');
      if (!('speechSynthesis' in window)) {
        setTimeout(() => {
          this.stopSpeaking();
          if (onComplete) onComplete();
        }, 2000);
        return;
      }

      const langMap = {
        'hi': 'hi-IN', 'hinglish': 'hi-IN', 'gu': 'gu-IN', 'mr': 'mr-IN',
        'ta': 'ta-IN', 'te': 'te-IN', 'bn': 'bn-IN', 'pa': 'pa-IN',
        'kn': 'kn-IN', 'ml': 'ml-IN', 'ur': 'ur-PK', 'en': 'en-IN'
      };

      const curLang = lang || window.selectedLanguage || localStorage.getItem('preferred_lang') || 'en';
      const targetLocale = langMap[curLang] || 'en-IN';
      const langPrefix = targetLocale.substring(0, 2);

      const utterance = new SpeechSynthesisUtterance(cleanVoiceText);
      utterance.rate = 0.95;
      utterance.pitch = this.role === 'student' ? 1.05 : this.role === 'principal' ? 0.92 : this.role === 'parent' ? 1.0 : 1.0;
      utterance.lang = targetLocale;

      // High-precision regional voice matcher
      const voices = window.speechSynthesis.getVoices();
      if (voices && voices.length > 0) {
        let selectedVoice = voices.find(v => v.lang.replace('_', '-') === targetLocale) ||
                            voices.find(v => v.lang.replace('_', '-').startsWith(langPrefix)) ||
                            voices.find(v => v.name.toLowerCase().includes(curLang));

        // For Indic languages (Hindi, Gujarati, Marathi, Punjabi, Bengali, Hinglish),
        // fallback to Hindi (hi-IN) voice with native Devanagari/Indic phonemes, NEVER an English voice!
        if (!selectedVoice && ['hi', 'hinglish', 'gu', 'mr', 'pa', 'bn'].includes(curLang)) {
          selectedVoice = voices.find(v => v.lang.startsWith('hi') || v.name.toLowerCase().includes('hindi') || v.name.toLowerCase().includes('kalpana') || v.name.toLowerCase().includes('hemant') || v.name.toLowerCase().includes('madhur') || v.name.toLowerCase().includes('swara'));
        }

        // For Tamil, Telugu, Kannada, Malayalam, fallback to South-Asian Dravidian voice
        if (!selectedVoice && ['ta', 'te', 'kn', 'ml'].includes(curLang)) {
          selectedVoice = voices.find(v => v.lang.startsWith(langPrefix) || v.lang.startsWith('hi') || v.name.toLowerCase().includes('india'));
        }

        // Fallback for English
        if (!selectedVoice) {
          selectedVoice = voices.find(v => v.name.includes("Google") || v.name.includes("Natural") || v.lang === 'en-IN' || v.lang === 'en-US') || voices[0];
        }

        if (selectedVoice) {
          utterance.voice = selectedVoice;
          utterance.lang = selectedVoice.lang || targetLocale;
        }
      }

      utterance.onend = () => {
        this.stopSpeaking();
        if (onComplete) onComplete();
      };

      utterance.onerror = () => {
        this.stopSpeaking();
        if (onComplete) onComplete();
      };

      window.speechSynthesis.speak(utterance);
    }

    stopSpeaking() {
      clearInterval(this.visemeInterval);
      this.setState('idle');
      this.mouthOpenTarget = 0.05;
      this.mouthWidthTarget = 1.0;
      this.headTiltTarget = 0;
    }

    startAnimationLoop() {
      const render = () => {
        this.time += 0.03;
        this.updatePhysics();
        this.draw();
        this.animationFrame = requestAnimationFrame(render);
      };
      render();
    }

    updatePhysics() {
      // Smooth lerping for natural organic motion
      this.mouthOpen += (this.mouthOpenTarget - this.mouthOpen) * 0.3;
      this.mouthWidth += (this.mouthWidthTarget - this.mouthWidth) * 0.3;
      this.headTilt += (this.headTiltTarget - this.headTilt) * 0.1;
    }

    draw() {
      const ctx = this.ctx;
      const w = this.width;
      const h = this.height;
      if (!ctx || !w || !h) return;

      ctx.clearRect(0, 0, w, h);
      const p = this.palettes[this.role] || this.palettes.student;

      const cx = w / 2;
      const cy = h / 2 - 10;
      const breath = Math.sin(this.time * 2) * 3;

      // 1. Studio Radial Backdrop & Aura Glow
      const bgGrad = ctx.createRadialGradient(cx, cy, 20, cx, cy, 180);
      bgGrad.addColorStop(0, p.aura + '28');
      bgGrad.addColorStop(0.6, p.accent + '10');
      bgGrad.addColorStop(1, 'transparent');
      ctx.fillStyle = bgGrad;
      ctx.fillRect(0, 0, w, h);

      // 2. Animated Voice Equalizer Waves at Base when Speaking
      if (this.state === 'speaking') {
        ctx.fillStyle = p.aura + 'bb';
        const barCount = 18;
        const startX = cx - 70;
        for (let i = 0; i < barCount; i++) {
          const barHeight = Math.abs(Math.sin(this.time * 6 + i * 0.5)) * 24 + 4;
          ctx.fillRect(startX + i * 8, h - 35 - barHeight / 2, 4, barHeight);
        }
      }

      // State Ring
      if (this.state === 'speaking' || this.state === 'listening') {
        ctx.strokeStyle = this.state === 'speaking' ? p.aura : '#22c55e';
        ctx.lineWidth = 2.5;
        ctx.setLineDash([8, 6]);
        ctx.lineDashOffset = -this.time * 20;
        ctx.beginPath();
        ctx.arc(cx, cy + breath, 105, 0, Math.PI * 2);
        ctx.stroke();
        ctx.setLineDash([]);
      }

      ctx.save();
      ctx.translate(cx, cy + breath);
      ctx.rotate(this.headTilt);

      // 2. Shoulders / Collar
      ctx.fillStyle = '#1e293b';
      ctx.beginPath();
      ctx.ellipse(0, 115, 85, 45, 0, 0, Math.PI * 2);
      ctx.fill();

      // Tie / Collar Accent
      ctx.fillStyle = p.tie;
      ctx.beginPath();
      ctx.moveTo(-12, 75);
      ctx.lineTo(12, 75);
      ctx.lineTo(6, 120);
      ctx.lineTo(0, 130);
      ctx.lineTo(-6, 120);
      ctx.closePath();
      ctx.fill();

      // 3. Neck
      ctx.fillStyle = '#fbd38d';
      ctx.fillRect(-18, 45, 36, 40);

      // 4. Head Base
      ctx.fillStyle = '#fce7b2';
      ctx.beginPath();
      ctx.ellipse(0, 0, 68, 78, 0, 0, Math.PI * 2);
      ctx.fill();

      // Hair
      ctx.fillStyle = '#1e1e24';
      ctx.beginPath();
      ctx.ellipse(0, -35, 72, 50, 0, Math.PI, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.ellipse(-55, -15, 18, 40, 0.2, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.ellipse(55, -15, 18, 40, -0.2, 0, Math.PI * 2);
      ctx.fill();

      // 5. Eyebrows
      ctx.strokeStyle = '#2d3748';
      ctx.lineWidth = 3.5;
      ctx.beginPath();
      if (this.state === 'thinking') {
        ctx.moveTo(-42, -28);
        ctx.quadraticCurveTo(-26, -38, -12, -26);
        ctx.moveTo(12, -26);
        ctx.quadraticCurveTo(26, -34, 42, -32);
      } else {
        ctx.moveTo(-42, -30);
        ctx.quadraticCurveTo(-26, -36, -12, -30);
        ctx.moveTo(12, -30);
        ctx.quadraticCurveTo(26, -36, 42, -30);
      }
      ctx.stroke();

      // 6. Eyes (with organic blinking)
      const eyeOpen = Math.max(0.08, 1 - this.blinkProgress);
      // Left Eye
      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.ellipse(-26, -12, 14, 11 * eyeOpen, 0, 0, Math.PI * 2);
      ctx.fill();
      // Right Eye
      ctx.beginPath();
      ctx.ellipse(26, -12, 14, 11 * eyeOpen, 0, 0, Math.PI * 2);
      ctx.fill();

      if (eyeOpen > 0.3) {
        // Iris / Pupils
        ctx.fillStyle = p.accent;
        ctx.beginPath();
        ctx.arc(-26 + this.eyeGazeX, -12 + this.eyeGazeY, 6, 0, Math.PI * 2);
        ctx.arc(26 + this.eyeGazeX, -12 + this.eyeGazeY, 6, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#0f172a';
        ctx.beginPath();
        ctx.arc(-26 + this.eyeGazeX, -12 + this.eyeGazeY, 3, 0, Math.PI * 2);
        ctx.arc(26 + this.eyeGazeX, -12 + this.eyeGazeY, 3, 0, Math.PI * 2);
        ctx.fill();

        // Eye Catchlight
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(-28, -14, 2, 0, Math.PI * 2);
        ctx.arc(24, -14, 2, 0, Math.PI * 2);
        ctx.fill();
      }

      // 7. Nose
      ctx.strokeStyle = '#d69e2e';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(0, -6);
      ctx.lineTo(3, 14);
      ctx.lineTo(-2, 16);
      ctx.stroke();

      // 8. Dynamic Viseme Lip-Sync Mouth
      const mOpen = this.mouthOpen * 26;
      const mWidth = this.mouthWidth * 24;

      if (this.mouthOpen > 0.15) {
        // Open Mouth / Speaking
        ctx.fillStyle = '#742a2a';
        ctx.beginPath();
        ctx.ellipse(0, 34, mWidth, mOpen, 0, 0, Math.PI * 2);
        ctx.fill();

        // Teeth upper
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.ellipse(0, 34 - mOpen * 0.6, mWidth * 0.7, mOpen * 0.35, 0, 0, Math.PI * 2);
        ctx.fill();

        // Tongue
        ctx.fillStyle = '#e53e3e';
        ctx.beginPath();
        ctx.ellipse(0, 34 + mOpen * 0.45, mWidth * 0.6, mOpen * 0.4, 0, 0, Math.PI * 2);
        ctx.fill();

        // Lip outline
        ctx.strokeStyle = '#c53030';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.ellipse(0, 34, mWidth, mOpen, 0, 0, Math.PI * 2);
        ctx.stroke();
      } else {
        // Closed / Gentle smile
        ctx.strokeStyle = '#9b2c2c';
        ctx.lineWidth = 2.8;
        ctx.beginPath();
        ctx.moveTo(-16, 32);
        ctx.quadraticCurveTo(0, 38, 16, 32);
        ctx.stroke();
      }

      ctx.restore();
    }

    destroy() {
      if (this.blinkTimer) clearTimeout(this.blinkTimer);
      if (this.visemeInterval) clearInterval(this.visemeInterval);
      if (this.animationFrame) cancelAnimationFrame(this.animationFrame);
    }
  }

  global.SchoolAvatarController = SchoolAvatarController;
})(window);
