<template>
    <logo class="logo"></logo>
    <div class="view">
        <div class="default-text">Registration</div>
        <div class="form">
            <div class="gray-text">start the bot at the link</div>
            <a :href="'https://t.me/t0d0d0d0bot?start='+authcode_bot" target="_blank" rel="noopener noreferrer" class="link">telegram bot</a>
            <router-link class="referer" to="/login">log in</router-link>
            <div class="error">{{ error }}</div>
        </div>
    </div>
</template>


<script setup>
import { RouterLink } from 'vue-router'
import Logo from '../components/Logo.vue'
import { ref, onMounted } from 'vue'
import { request } from '@/modules/requester'

const authcode = ref('')
const name = ref('') 
const error = ref('') 

const authcode_bot = ref('') 

async function signup() {
    let r = await request('/user/signup', 'POST', {name:name.value, authcode:authcode.value}, false, false)
    if (r.type === 'error' && r.message === 'Auth Code Error' | r.message === 'Auth Error') {
        error.value = r.desc
    } else {
        localStorage.setItem('private_key', r.data[0].private_key)
        error.value = ''
        window.location = '/overview'
    }
}


onMounted(async ()=> {

    let r = await request('/user/authcode/new', 'POST', {})
    authcode_bot.value = r.data[0].authcode

    async function check() {
        let r = await request('/user/authcode/signup', 'POST', {authcode:authcode_bot.value}, false, false)
        console.log(r);
        
        if (r.type != 'error') {
            clearInterval(intervalId)

            localStorage.setItem('private_key', r.data[0].private_key)
            error.value = ''
            window.location = '/overview'
        }


    }

    const intervalId = setInterval(check, 500);

})


</script>


<style>
#app{
    align-items: center;
    }
    </style>

<style scoped>


    .logo{
    margin-top: 150px;
    margin-bottom: 20px;
    }
    .view{
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        }
    @media (max-width: 750px) {
        .logo{
            position: fixed;
            margin-top: 0;
        }
        .view{
            justify-content: center;
        }
    }

    .default-text{
        margin-bottom: 20px;
    }
    .form{
        display: flex;
        flex-direction: column;
        padding: 10px;
        border: var(--gray-color) solid 1px;
        gap: 10px;
        box-sizing: border-box;
    }
    a{
        text-decoration: none;
        color: var(--black-color);
        padding: 10px;
        background-color: var(--blue-color);
    }
    a:hover{
        background-color: var(--black-color);
        color: var(--blue-color);
        outline:1px solid var(--blue-color);
        outline-offset:-1px;
    }

    input, button{
        border-color: none;
        padding: 10px;
        background-color: var(--black-color);
        border: var(--gray-color) solid 1px;
        color: var(--white-color);
        font-family: "Source Code Pro", monospace;
        font-size: 16px;
    }
    input:hover, button:hover{
        background-color: var(--gray-color);
        color: var(--black-color);
    }

    input:focus, button {
        outline: none;
    }
    .button{
        border: none;
        background-color: var(--green-color);
        color: var(--black-color);
    }
    .button:hover{
        background-color: var(--black-color);
        outline:1px solid var(--green-color);
        outline-offset:-1px;
        color: var(--green-color);
    }
    .referer{
        background-color: var(--black-color);
        color: var(--white-color);
        outline:1px dashed var(--gray-color);
        outline-offset:-1px;
    }
    .referer:hover{
        background-color: var(--gray-color);
        outline:none;
        color: var(--black-color);
    }

    .error {
        color:var(--red-color);
    }

</style>