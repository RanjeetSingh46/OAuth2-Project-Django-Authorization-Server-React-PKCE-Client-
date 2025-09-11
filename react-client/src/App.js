import React, {useEffect, useState} from 'react';
import {OAUTH_CLIENT_ID, OAUTH_REDIRECT_URI, OAUTH_AUTH_URL, API_USERINFO_URL} from './config';
import {generatePKCECodes} from './pkce';

async function exchangeCodeForToken(code){
  const verifier = localStorage.getItem('pkce_verifier');
  console.log('PKCE Debug - Verifier from localStorage:', verifier);
  console.log('PKCE Debug - Code received:', code);
  
  if (!verifier) {
    console.error('PKCE Error: No verifier found in localStorage!');
    return {error: 'No PKCE verifier found'};
  }
  
  const params = new URLSearchParams();
  params.append('grant_type','authorization_code');
  params.append('code', code);
  params.append('redirect_uri', OAUTH_REDIRECT_URI);
  params.append('client_id', OAUTH_CLIENT_ID);
  params.append('code_verifier', verifier);
  
  console.log('PKCE Debug - Token request params:', params.toString());
  
  const res = await fetch('http://localhost:8000/o/token/',{
    method: 'POST', 
    headers: {'Content-Type':'application/x-www-form-urlencoded'}, 
    body: params.toString()
  });
  
  const result = await res.json();
  console.log('PKCE Debug - Token response:', result);
  return result;
}

export default function App(){
  const [token,setToken]=useState(localStorage.getItem('access_token')||null);
  const [profile,setProfile]=useState(null);
  const [loading, setLoading] = useState(false);
  
  useEffect(()=>{
    const params=new URLSearchParams(window.location.search);
    const code=params.get('code');
    if(code && !token){
      setLoading(true);
      exchangeCodeForToken(code).then(data=>{
        if(data.access_token){
          localStorage.setItem('access_token',data.access_token);
          localStorage.setItem('refresh_token',data.refresh_token||'');
          setToken(data.access_token);
          window.history.replaceState({}, document.title, '/');
        } else console.error('Token error',data);
        setLoading(false);
      });
    }
  },[token]);

  const login=async()=>{
    setLoading(true);
    try {
      const {verifier,challenge}=await generatePKCECodes();
      console.log('PKCE Debug - Generated verifier:', verifier);
      console.log('PKCE Debug - Generated challenge:', challenge);
      
      localStorage.setItem('pkce_verifier',verifier);
      console.log('PKCE Debug - Stored verifier in localStorage');
      
      const params=new URLSearchParams({response_type:'code',client_id:OAUTH_CLIENT_ID,redirect_uri:OAUTH_REDIRECT_URI,scope:'read',code_challenge:challenge,code_challenge_method:'S256'});
      console.log('PKCE Debug - Authorization params:', params.toString());
      
      window.location = `${OAUTH_AUTH_URL}?${params.toString()}`;
    } catch (error) {
      console.error('Login error:', error);
      setLoading(false);
    }
  };

  const fetchProfile=async()=>{
    setLoading(true);
    try {
      const t = localStorage.getItem('access_token');
      const r = await fetch(API_USERINFO_URL, {headers: {Authorization: `Bearer ${t}`}});
      if(r.ok) setProfile(await r.json()); else setProfile({error:'Failed to fetch profile'});
    } catch (error) {
      setProfile({error: 'Network error occurred'});
    }
    setLoading(false);
  };

  const logout=async()=>{
    setLoading(true);
    try {
      const t = localStorage.getItem('access_token');
      await fetch('http://localhost:8000/api/logout/', {method:'POST', headers:{Authorization:`Bearer ${t}`}});
    } catch (error) {
      console.error('Logout error:', error);
    }
    localStorage.removeItem('access_token'); 
    localStorage.removeItem('refresh_token'); 
    setToken(null); 
    setProfile(null);
    setLoading(false);
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.header}>
          <h1 style={styles.title}>OAuth Authentication</h1>
          <p style={styles.subtitle}>Secure PKCE Implementation</p>
        </div>
        
        <div style={styles.content}>
          {!token ? (
            <div style={styles.loginSection}>
              <div style={styles.iconContainer}>
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" style={styles.icon}>
                  <path d="M12 1L3 5V11C3 16.55 6.84 21.74 12 23C17.16 21.74 21 16.55 21 11V5L12 1Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <path d="M9 12L11 14L15 10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
              <h2 style={styles.welcomeTitle}>Welcome Back</h2>
              <p style={styles.welcomeText}>Sign in to your account to continue</p>
              <button 
                onClick={login} 
                disabled={loading}
                style={{
                  ...styles.button,
                  ...styles.primaryButton,
                  ...(loading ? styles.buttonDisabled : {})
                }}
              >
                {loading ? (
                  <div style={styles.spinner}></div>
                ) : (
                  <>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" style={styles.buttonIcon}>
                      <path d="M15 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      <path d="M10 17L15 12L10 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      <path d="M15 12H3" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                    Sign In with PKCE
                  </>
                )}
              </button>
            </div>
          ) : (
            <div style={styles.dashboardSection}>
              <div style={styles.statusBadge}>
                <div style={styles.statusIndicator}></div>
                <span style={styles.statusText}>Authenticated</span>
              </div>
              
              <div style={styles.actionButtons}>
                <button 
                  onClick={fetchProfile} 
                  disabled={loading}
                  style={{
                    ...styles.button,
                    ...styles.secondaryButton,
                    ...(loading ? styles.buttonDisabled : {})
                  }}
                >
                  {loading ? (
                    <div style={styles.spinner}></div>
                  ) : (
                    <>
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" style={styles.buttonIcon}>
                        <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                        <circle cx="12" cy="7" r="4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      </svg>
                      Fetch Profile
                    </>
                  )}
                </button>
                
                <button 
                  onClick={logout} 
                  disabled={loading}
                  style={{
                    ...styles.button,
                    ...styles.dangerButton,
                    ...(loading ? styles.buttonDisabled : {})
                  }}
                >
                  {loading ? (
                    <div style={styles.spinner}></div>
                  ) : (
                    <>
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" style={styles.buttonIcon}>
                        <path d="M9 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                        <path d="M16 17L21 12L16 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                        <path d="M21 12H9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      </svg>
                      Sign Out
                    </>
                  )}
                </button>
              </div>
              
              {profile && (
                <div style={styles.profileSection}>
                  <h3 style={styles.profileTitle}>Profile Information</h3>
                  <div style={styles.profileCard}>
                    {profile.error ? (
                      <div style={styles.errorMessage}>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" style={styles.errorIcon}>
                          <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2"/>
                          <path d="M15 9L9 15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                          <path d="M9 9L15 15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                        </svg>
                        {profile.error}
                      </div>
                    ) : (
                      <pre style={styles.profileData}>{JSON.stringify(profile, null, 2)}</pre>
                    )}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '20px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
  },
  card: {
    background: 'rgba(255, 255, 255, 0.95)',
    borderRadius: '20px',
    boxShadow: '0 25px 50px rgba(0, 0, 0, 0.25)',
    backdropFilter: 'blur(10px)',
    border: '1px solid rgba(255, 255, 255, 0.2)',
    maxWidth: '500px',
    width: '100%',
    overflow: 'hidden'
  },
  header: {
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    padding: '30px',
    textAlign: 'center'
  },
  title: {
    margin: '0 0 8px 0',
    fontSize: '28px',
    fontWeight: '700',
    letterSpacing: '-0.5px'
  },
  subtitle: {
    margin: '0',
    fontSize: '16px',
    opacity: '0.9',
    fontWeight: '400'
  },
  content: {
    padding: '40px 30px'
  },
  loginSection: {
    textAlign: 'center'
  },
  iconContainer: {
    marginBottom: '24px'
  },
  icon: {
    color: '#667eea',
    filter: 'drop-shadow(0 2px 4px rgba(102, 126, 234, 0.2))'
  },
  welcomeTitle: {
    margin: '0 0 8px 0',
    fontSize: '24px',
    fontWeight: '600',
    color: '#2d3748'
  },
  welcomeText: {
    margin: '0 0 32px 0',
    fontSize: '16px',
    color: '#718096',
    lineHeight: '1.5'
  },
  dashboardSection: {
    display: 'flex',
    flexDirection: 'column',
    gap: '24px'
  },
  statusBadge: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '8px',
    background: '#f0fff4',
    border: '1px solid #9ae6b4',
    borderRadius: '25px',
    padding: '8px 16px',
    alignSelf: 'center'
  },
  statusIndicator: {
    width: '8px',
    height: '8px',
    borderRadius: '50%',
    background: '#38a169'
  },
  statusText: {
    fontSize: '14px',
    fontWeight: '500',
    color: '#38a169'
  },
  actionButtons: {
    display: 'flex',
    gap: '12px',
    flexDirection: 'column'
  },
  button: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '8px',
    padding: '14px 24px',
    borderRadius: '12px',
    border: 'none',
    fontSize: '16px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.2s ease',
    minHeight: '52px',
    textDecoration: 'none',
    margin: '0 auto',
    width: 'fit-content'
  },
  primaryButton: {
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    boxShadow: '0 4px 15px rgba(102, 126, 234, 0.4)'
  },
  secondaryButton: {
    background: '#f7fafc',
    color: '#4a5568',
    border: '1px solid #e2e8f0'
  },
  dangerButton: {
    background: '#fed7d7',
    color: '#c53030',
    border: '1px solid #feb2b2'
  },
  buttonDisabled: {
    opacity: '0.6',
    cursor: 'not-allowed'
  },
  buttonIcon: {
    flexShrink: 0
  },
  spinner: {
    width: '20px',
    height: '20px',
    border: '2px solid transparent',
    borderTop: '2px solid currentColor',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite'
  },
  profileSection: {
    marginTop: '8px'
  },
  profileTitle: {
    margin: '0 0 16px 0',
    fontSize: '18px',
    fontWeight: '600',
    color: '#2d3748'
  },
  profileCard: {
    background: '#f7fafc',
    border: '1px solid #e2e8f0',
    borderRadius: '12px',
    padding: '20px',
    maxHeight: '300px',
    overflow: 'auto'
  },
  profileData: {
    margin: '0',
    fontSize: '14px',
    lineHeight: '1.5',
    color: '#4a5568',
    fontFamily: 'Monaco, Menlo, "Ubuntu Mono", monospace',
    whiteSpace: 'pre-wrap',
    wordBreak: 'break-word'
  },
  errorMessage: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    color: '#c53030',
    fontSize: '14px',
    fontWeight: '500'
  },
  errorIcon: {
    flexShrink: 0,
    color: '#c53030'
  }
};

// Add CSS animation for spinner
const spinKeyframes = `
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
`;

// Inject the keyframes into the document
if (typeof document !== 'undefined') {
  const styleSheet = document.createElement('style');
  styleSheet.textContent = spinKeyframes;
  document.head.appendChild(styleSheet);
}