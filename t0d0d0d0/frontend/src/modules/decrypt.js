import forge from 'node-forge';


export function decrypt(objs, encrypted) {
    encrypted = encrypted || []
    let decrypted = []
    
    for (let i = 0; i < objs.length; i++) {
        let obj = {}
        for (let [name, val] of Object.entries(objs[i])) {
            if (encrypted.includes(name) && val) {
                val = decryptRSA(val, localStorage.getItem('private_key'))
            }
            obj[name] = val
        }
        decrypted.push(obj)
    }
    return {data:decrypted}
}


function decryptRSA(encryptedData, privateKeyPem) {
    const privateKey = forge.pki.privateKeyFromPem(privateKeyPem);
    const encryptedBytes = forge.util.decode64(encryptedData);
    console.log(encryptedData);
    
    const decryptedBytes = privateKey.decrypt(encryptedBytes, 'RSA-OAEP', {
    md: forge.md.sha256.create(),
    mgf1: { md: forge.md.sha256.create() }
});

const decrypted = forge.util.decodeUtf8(decryptedBytes);

    return decrypted;
}

