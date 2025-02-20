import axios from 'axios';
import { decrypt } from './decrypt';

async function jwtChecker(response, isRefresh=false) {
    if (response.type === 'error' && response.message == 'JWT Error') {
        if (isRefresh) {
            window.location = '/'
        } else {
            let req = await fetch(`/api/user/refresh`, {method: 'POST', headers:new Headers().append("Content-Type", "application/json")})
            let res = await req.json()
            await jwtChecker(res, true)            
        }
    }
}


export async function request(path, method, data, jwtcheck=false, decrypte=true) {
    // const body = JSON.stringify(data)
    // console.log(data, JSON.parse(body));
    // const headers = new Headers().append("Content-Type", "application/json;charset=utf-8")
    // let req = await fetch(`/api/${path}`, {method: method, body:body, headers:headers})
    // let res = await req.json()
    // if (jwtcheck) {
    //     await jwtChecker(res)
    // }
    // return res
    try {
        const response = await axios({
            method: method,
            url: `/api${path}`,
            data: data,
            headers: {'Content-Type': 'application/json;charset=utf-8'}
        });
        const res = response.data;
        
        if (decrypte) {
            return decrypt(res.data, res.encrypted)
        } return res
        
    } catch (error) {
        const response = error.response.data
        const res = response;
    
        if (jwtcheck && res.type === 'error' && res.message == 'JWT Error') {
            const req = await fetch(`/api/user/refresh`, {method: 'POST', headers:new Headers().append("Content-Type", "application/json")})
            const res2 = await req.json()
            if (res2.type === 'error' && res2.message == 'JWT Error') {
                window.location = '/login'
            } else{
                const response = await axios({
                    method: method,
                    url: `/api${path}`,
                    data: data,
                    headers: {'Content-Type': 'application/json;charset=utf-8'}
                });
                const res = response.data;
                return res
            }
        }
        if (decrypte) {
            return decrypt(res.data, res.encrypted)
        } return res
    } 


}




