// pkce helpers
function base64urlencode(a){return btoa(String.fromCharCode.apply(null,new Uint8Array(a))).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');}
async function sha256(data){const hash=await crypto.subtle.digest('SHA-256',data);return hash;}
export function generateRandomString(length=64){const arr=new Uint8Array(length);crypto.getRandomValues(arr);const chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~';let out='';for(let i=0;i<length;i++){out+=chars[arr[i]%chars.length];}return out;}
export async function pkceChallengeFromVerifier(v){const enc=new TextEncoder();const data=enc.encode(v);const digest=await sha256(data);return base64urlencode(digest);} 
export async function generatePKCECodes(){const verifier=generateRandomString(64);const challenge=await pkceChallengeFromVerifier(verifier);return {verifier,challenge};}
