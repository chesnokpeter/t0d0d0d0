<template>
    <div class="container">
        <logo class="logo"></logo>
        <menu-comp sel="projects" class="menu"></menu-comp>
        <div class="content">
            
        </div>
    </div>
</template>


<script setup>
import Logo from '../components/Logo.vue'
import { request } from '@/modules/requester'
import MenuComp from '../components/MenuComp.vue'
import { onMounted } from 'vue';


onMounted(async ()=> {
    // let r = request('/task/getInbox', 'GET', {}, true)
    // console.log(r);
})


// let r = await request('/task/getInbox', 'GET', jwtcheck=true)
// console.log(r);



</script>

<style>
#app{
    align-items: center;
}
</style>

<style scoped>
.inboxs {
    display: flex;
    flex-direction: column;
    color: var(--gray-color);
    gap: 10px;
}

.inbox {
    display: flex;
    /* flex-direction: column; */
    color: var(--white-color);
    gap: 10px;
    }
.inbox-item {
    outline:1px solid var(--gray-color);
    outline-offset:-1px;
    padding: 3.5px;
}

* {
    box-sizing: border-box;
}

.container {
    position: relative;
    margin-top: 150px; 
}

.logo {
    display: block;
    width: 100%; 
    /* height: 100%; */
    margin: 0 auto;
}

.menu {
    position: absolute;
    left: -100px;
}

@media (max-width: 750px) {
    .container {
        margin-top: 0px; 
    }
    .logo {
        width: 100%; 
        position: sticky;
        top: 0;
    }
    .menu {
        position: fixed;
        bottom: 0;
        width: 100%;
        left: 0;
    }

}

</style>