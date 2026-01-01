<template>
  <div class="about-view">
    <div class="about-container">
      <!-- Hero Section -->
      <div class="hero-section">
        <div class="hero-content">
          <h1 class="hero-title">Dream Entertainment</h1>
          <p class="hero-subtitle">Your Ultimate Movie & TV Show Database</p>
          <p class="hero-description">
            A comprehensive platform combining TMDB and IMDB data to deliver 
            the ultimate entertainment discovery experience.
          </p>
        </div>
        <div class="hero-decoration">
          <div class="decoration-circle"></div>
          <div class="decoration-circle"></div>
          <div class="decoration-circle"></div>
        </div>
      </div>

      <!-- Team Section -->
      <div class="section team-section">
        <div class="section-header">
          <h2 class="section-title">
            <span class="title-icon">👥</span>
            Our Creative Team
          </h2>
          <p class="section-subtitle">
            Meet the passionate developers behind this project
          </p>
        </div>

        <div class="team-grid">
          <!-- Member 1: Dhea -->
          <div class="team-card">
            <div class="member-profile">
              <div class="member-avatar">
                <!-- FOTO DHEA -->
                <img 
                  src="/team/Dhea.jpeg" 
                  alt="Dhea Meidiyana Windawati"
                  class="avatar-photo"
                  @error="handleImageError($event, 'D')"
                >
                <!-- Fallback ke inisial jika foto error -->
                <span class="avatar-fallback">D</span>
              </div>
            </div>
            <div class="card-body">
              <h3 class="member-name">Dhea Meidiyana Windawati</h3>
              <div class="member-info">
                <div class="info-item">
                  <span class="info-icon">🎓</span>
                  <span class="info-text">NIM: L0224004</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Member 2: Rambat -->
          <div class="team-card">
            <div class="member-profile">
              <div class="member-avatar">
                <!-- FOTO RAMBAT -->
                <img 
                  src="/team/Rambat.jpeg" 
                  alt="Rambat Ungu Aryati"
                  class="avatar-photo"
                  @error="handleImageError($event, 'R')"
                >
                <!-- Fallback ke inisial jika foto error -->
                <span class="avatar-fallback">R</span>
              </div>
            </div>
            <div class="card-body">
              <h3 class="member-name">Rambat Ungu Aryati</h3>
              <div class="member-info">
                <div class="info-item">
                  <span class="info-icon">🎓</span>
                  <span class="info-text">NIM: L0224010</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Project Info -->
      <div class="section project-section">
        <div class="section-header">
          <h2 class="section-title">
            <span class="title-icon">🚀</span>
            About This Project
          </h2>
          <p class="section-subtitle">
            Final Project for Database Systems Course
          </p>
        </div>

        <div class="project-content">
          <div class="project-card">
            <div class="card-icon">🎯</div>
            <h3 class="card-title">Project Vision</h3>
            <p class="card-text">
              Create a unified platform that combines data from TMDB and IMDB 
              databases, providing users with comprehensive entertainment 
              information in one seamless interface.
            </p>
          </div>

          <div class="project-card">
            <div class="card-icon">✨</div>
            <h3 class="card-title">Key Features</h3>
            <ul class="feature-list">
              <li><span class="check-icon">✓</span> Browse thousands of movies & TV shows</li>
              <li><span class="check-icon">✓</span> Advanced search & filtering system</li>
              <li><span class="check-icon">✓</span> Detailed information & ratings</li>
              <li><span class="check-icon">✓</span> Multi-database integration</li>
              <li><span class="check-icon">✓</span> Responsive design</li>
            </ul>
          </div>

          <div class="project-card">
            <div class="card-icon">🛠️</div>
            <h3 class="card-title">Tech Stack</h3>
            <div class="tech-stack">
              <div class="tech-category">
                <h4>Frontend</h4>
                <div class="tech-tags">
                  <span class="tech-tag">Vue.js</span>
                  <span class="tech-tag">CSS3</span>
                  <span class="tech-tag">JavaScript</span>
                </div>
              </div>
              <div class="tech-category">
                <h4>Backend</h4>
                <div class="tech-tags">
                  <span class="tech-tag">SQL Server</span>
                  <span class="tech-tag">Node.js</span>
                  <span class="tech-tag">REST API</span>
                </div>
              </div>
              <div class="tech-category">
                <h4>Data Sources</h4>
                <div class="tech-tags">
                  <span class="tech-tag">TMDB API</span>
                  <span class="tech-tag">IMDB Dataset</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Timeline -->
      <div class="section timeline-section">
        <div class="section-header">
          <h2 class="section-title">
            <span class="title-icon">📅</span>
            Development Timeline
          </h2>
        </div>
        <div class="timeline">
          <div class="timeline-item">
            <div class="timeline-date">Phase 1</div>
            <div class="timeline-content">
              <h3>Research & Planning</h3>
              <p>Database analysis, requirement gathering, and system design</p>
            </div>
          </div>
          <div class="timeline-item">
            <div class="timeline-date">Phase 2</div>
            <div class="timeline-content">
              <h3>Development</h3>
              <p>Frontend/backend development and database implementation</p>
            </div>
          </div>
          <div class="timeline-item">
            <div class="timeline-date">Phase 3</div>
            <div class="timeline-content">
              <h3>Testing</h3>
              <p>System testing and bug fixing</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="about-footer">
        <div class="footer-content">
          <h3>Dream Entertainment</h3>
          <p>Database Systems Final Project • 2025</p>
          <div class="footer-credits">
            <p>Created with ❤️ by Dhea & Rambat</p>
            <p class="footer-note">Universitas Sebelas Maret</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutView',
  methods: {
    handleImageError(event, initial) {
      // Sembunyikan gambar yang error
      event.target.style.display = 'none';
      
      // Tampilkan fallback (inisial)
      const fallback = event.target.nextElementSibling;
      if (fallback && fallback.classList.contains('avatar-fallback')) {
        fallback.style.display = 'flex';
      }
      
      console.warn(`Foto tidak ditemukan, menampilkan inisial ${initial}`);
    }
  }
}
</script>

<style scoped>
/* Base Styles */
.about-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f0c08 0%, #1a1612 100%);
  padding: 30px 20px;
  font-family: 'Poppins', sans-serif;
}

.about-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, 
    rgba(152, 57, 68, 0.1) 0%, 
    rgba(177, 79, 29, 0.1) 100%);
  border: 1px solid rgba(152, 57, 68, 0.2);
  border-radius: 24px;
  padding: 60px 40px;
  margin-bottom: 60px;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
}

.hero-title {
  font-size: 56px;
  background: linear-gradient(90deg, #983944, #b13f1d, #d88a64);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 20px;
  font-weight: 800;
  letter-spacing: 1px;
}

.hero-subtitle {
  font-size: 20px;
  color: #f8f4ed;
  margin-bottom: 25px;
  font-weight: 500;
  opacity: 0.9;
}

.hero-description {
  font-size: 16px;
  color: #d8a0a5;
  max-width: 700px;
  margin: 0 auto;
  line-height: 1.7;
}

.hero-decoration {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 1;
}

.decoration-circle {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(152, 57, 68, 0.1) 0%, transparent 70%);
}

.decoration-circle:nth-child(1) {
  width: 300px;
  height: 300px;
  top: -150px;
  right: -150px;
}

.decoration-circle:nth-child(2) {
  width: 200px;
  height: 200px;
  bottom: -100px;
  left: -100px;
}

.decoration-circle:nth-child(3) {
  width: 150px;
  height: 150px;
  top: 50%;
  left: 10%;
}

/* Section Common Styles */
.section {
  margin-bottom: 80px;
}

.section-header {
  text-align: center;
  margin-bottom: 50px;
}

.section-title {
  font-size: 36px;
  color: #f8f4ed;
  margin-bottom: 15px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.title-icon {
  font-size: 32px;
}

.section-subtitle {
  color: #d8a0a5;
  font-size: 18px;
  max-width: 600px;
  margin: 0 auto;
}

/* Team Section */
.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 30px;
  max-width: 1000px;
  margin: 0 auto;
}

.team-card {
  background: linear-gradient(135deg, 
    rgba(42, 36, 30, 0.8) 0%, 
    rgba(53, 45, 37, 0.8) 100%);
  border: 1px solid rgba(152, 57, 68, 0.3);
  border-radius: 20px;
  padding: 40px 30px;
  transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  backdrop-filter: blur(10px);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.team-card:hover {
  transform: translateY(-10px);
  border-color: rgba(152, 57, 68, 0.6);
  box-shadow: 
    0 20px 40px rgba(152, 57, 68, 0.15),
    0 0 40px rgba(152, 57, 68, 0.1);
}

.member-profile {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

/* AVATAR STYLE UNTUK FOTO */
.member-avatar {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  background: linear-gradient(135deg, #983944, #b13f1d);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 25px;
  overflow: hidden;
  border: 4px solid rgba(152, 57, 68, 0.3);
  position: relative;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.avatar-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.team-card:hover .avatar-photo {
  transform: scale(1.05);
}

.avatar-fallback {
  font-size: 60px;
  font-weight: bold;
  color: white;
  display: none;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #983944, #b13f1d);
}

.card-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  text-align: center;
}

.member-name {
  font-size: 24px;
  color: #f8f4ed;
  margin-bottom: 20px;
  font-weight: 600;
  line-height: 1.3;
}

.member-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  align-items: center;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 10px;
  justify-content: center;
}

.info-icon {
  font-size: 16px;
  opacity: 0.8;
}

.info-text {
  color: #d8a0a5;
  font-size: 16px;
  font-weight: 500;
}

/* Project Section */
.project-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.project-card {
  background: rgba(42, 36, 30, 0.6);
  border: 1px solid rgba(152, 57, 68, 0.3);
  border-radius: 16px;
  padding: 30px;
  transition: all 0.3s ease;
}

.project-card:hover {
  border-color: rgba(152, 57, 68, 0.6);
  transform: translateY(-5px);
}

.card-icon {
  font-size: 40px;
  margin-bottom: 20px;
}

.card-title {
  font-size: 20px;
  color: #f8f4ed;
  margin-bottom: 15px;
  font-weight: 600;
}

.card-text {
  color: #d8a0a5;
  line-height: 1.6;
  font-size: 14px;
}

.feature-list {
  list-style: none;
  padding: 0;
}

.feature-list li {
  color: #d8a0a5;
  padding: 8px 0;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.check-icon {
  color: #b13f1d;
  font-weight: bold;
}

.tech-stack {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.tech-category h4 {
  color: #f8f4ed;
  font-size: 16px;
  margin-bottom: 10px;
  font-weight: 600;
}

.tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tech-tag {
  background: rgba(152, 57, 68, 0.15);
  border: 1px solid rgba(152, 57, 68, 0.3);
  color: #d8a0a5;
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 12px;
}

/* Timeline */
.timeline {
  max-width: 800px;
  margin: 0 auto;
}

.timeline-item {
  display: flex;
  gap: 30px;
  margin-bottom: 40px;
  position: relative;
}

.timeline-item:not(:last-child)::after {
  content: '';
  position: absolute;
  left: 100px;
  top: 50px;
  bottom: -40px;
  width: 2px;
  background: rgba(152, 57, 68, 0.3);
}

.timeline-date {
  min-width: 100px;
  background: rgba(152, 57, 68, 0.2);
  border: 1px solid rgba(152, 57, 68, 0.4);
  color: #d8a0a5;
  padding: 10px 20px;
  border-radius: 20px;
  text-align: center;
  font-weight: 600;
  font-size: 14px;
}

.timeline-content {
  flex: 1;
}

.timeline-content h3 {
  color: #f8f4ed;
  font-size: 20px;
  margin-bottom: 10px;
  font-weight: 600;
}

.timeline-content p {
  color: #d8a0a5;
  font-size: 14px;
  line-height: 1.6;
}

/* Footer */
.about-footer {
  margin-top: 80px;
  padding-top: 40px;
  border-top: 1px solid rgba(152, 57, 68, 0.3);
  text-align: center;
}

.footer-content h3 {
  color: #f8f4ed;
  font-size: 24px;
  margin-bottom: 10px;
  font-weight: 600;
}

.footer-content p {
  color: #d8a0a5;
  margin-bottom: 10px;
}

.footer-credits p {
  color: #b87c7c;
  font-size: 14px;
  margin: 5px 0;
}

.footer-note {
  font-size: 12px;
  opacity: 0.7;
  margin-top: 15px;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-title {
    font-size: 40px;
  }
  
  .section-title {
    font-size: 28px;
  }
  
  .team-grid,
  .project-content {
    grid-template-columns: 1fr;
  }
  
  .timeline-item {
    flex-direction: column;
    gap: 15px;
  }
  
  .timeline-item:not(:last-child)::after {
    left: 20px;
    top: 100px;
  }
  
  .member-avatar {
    width: 140px;
    height: 140px;
  }
  
  .avatar-fallback {
    font-size: 50px;
  }
}

@media (max-width: 480px) {
  .hero-section {
    padding: 40px 20px;
  }
  
  .hero-title {
    font-size: 32px;
  }
  
  .team-card,
  .project-card {
    padding: 20px;
  }
  
  .member-avatar {
    width: 120px;
    height: 120px;
  }
  
  .avatar-fallback {
    font-size: 40px;
  }
  
  .member-name {
    font-size: 20px;
  }
}
</style>