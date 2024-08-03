
async function jwtChecker(response, isRefresh=false) {
    if (response.type === 'error' && response.message == 'JWT Error') {
        if (isRefresh) {
            window.location = '/'
        } else {
            let req = await fetch(`/api/user/refresh`, {method: 'POST', headers:new Headers().append("Content-Type", "application/json")})
            let res = await req.json()
            await jwtChecker(res, isRefresh=True)            
        }
    }
}


export async function request(path, method, data, jwtcheck=false) {
    const body = JSON.stringify(data)
    const headers = new Headers().append("Content-Type", "application/json")
    let req = await fetch(`/api${path}`, {method: method, body:body, headers:headers})
    let res = await req.json()
    if (jwtCheck) {
        await jwtChecker(res)
    }
    return res
}



