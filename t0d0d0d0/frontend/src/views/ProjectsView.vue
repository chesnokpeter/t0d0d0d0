<template>
    <div class="container">
        <logo class="logo"></logo>
        <menu-comp sel="projects" class="menu"></menu-comp>
        <div class="content">
            <div class="project" v-for="(project, index) in projects" :key="index">{{ project }}</div>
        </div>
    </div>
</template>


<script setup>
import Logo from '../components/Logo.vue'
import { request } from '@/modules/requester'
import MenuComp from '../components/MenuComp.vue'
import { onMounted, ref } from 'vue';

let projects = ref([])

onMounted(async ()=> {
    let r = await request('/project/getProjects', 'GET', {}, true)
    for (let i = 0; i < r.data.length; i++) {
        projects.value.push(r.data[i].name)
        
    }
})





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

.content {
    display: flex;
    gap: 10px;
    max-width: 600px;
    display: flex;
    flex-wrap: wrap;
}

.project {
    outline:1px solid var(--gray-color);
    outline-offset:-1px;
    padding: 3.5px;
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
        flex-direction: row;
        justify-content: space-between;
    }
    

}

</style>