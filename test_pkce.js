const crypto = require('crypto');

// Replicate the React PKCE functions in Node.js
function base64urlencode(buffer) {
    return buffer.toString('base64')
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=/g, '');
}

function sha256(plain) {
    return crypto.createHash('sha256').update(plain).digest();
}

function generateRandomString(length = 64) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~';
    let result = '';
    const randomBytes = crypto.randomBytes(length);
    
    for (let i = 0; i < length; i++) {
        result += chars[randomBytes[i] % chars.length];
    }
    return result;
}

function pkceChallengeFromVerifier(verifier) {
    const hash = sha256(verifier);
    return base64urlencode(hash);
}

async function generatePKCECodes() {
    const verifier = generateRandomString(64);
    const challenge = pkceChallengeFromVerifier(verifier);
    return { verifier, challenge };
}

// Test PKCE generation
async function testPKCE() {
    console.log('Testing PKCE generation...');
    
    const testCodes = await generatePKCECodes();
    console.log('Generated verifier:', testCodes.verifier);
    console.log('Generated challenge:', testCodes.challenge);
    console.log('Verifier length:', testCodes.verifier.length);
    console.log('Challenge length:', testCodes.challenge.length);
    
    // Test the verification manually
    const testVerifier = testCodes.verifier;
    const testChallenge = testCodes.challenge;
    const regeneratedChallenge = pkceChallengeFromVerifier(testVerifier);
    
    console.log('\nVerification test:');
    console.log('Original challenge:', testChallenge);
    console.log('Regenerated challenge:', regeneratedChallenge);
    console.log('Match:', testChallenge === regeneratedChallenge);
    
    // Test with a known verifier/challenge pair
    const knownVerifier = 'test_verifier_12345_abcdef_this_is_a_test_verifier_for_pkce_validation';
    const knownChallenge = pkceChallengeFromVerifier(knownVerifier);
    console.log('\nKnown test case:');
    console.log('Known verifier:', knownVerifier);
    console.log('Known challenge:', knownChallenge);
}

// Run the test
testPKCE().catch(console.error);
