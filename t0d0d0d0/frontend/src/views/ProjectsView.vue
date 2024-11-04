<template>
    <div class="container">
        <logo class="logo"></logo>
        <menu-comp sel="projects" class="menu"></menu-comp>
        <div class="content">
            <input class="project-new" type="button" value="+" @click="addNewProject()"> <div class="project" v-for="(project, index) in projects" :key="index" @click="openModal(project.name, project.id)">{{ project.name }}</div>
        </div>
    </div>

    <ProjectModal v-if="showModal" @close="closeModal" :id="idModal" :name="nameModal"/>

</template>


<script setup>
import Logo from '../components/Logo.vue'
import { request } from '@/modules/requester'
import MenuComp from '../components/MenuComp.vue'
import { onMounted, ref } from 'vue';
import ProjectModal from '@/components/ProjectModal.vue';

const showModal = ref(false)
const idModal = ref()
const nameModal = ref()

const projects = ref([])

onMounted(async ()=> {
    let r = await request('/project/get', 'GET', {}, true)
    for (let i = 0; i < r.data.length; i++) {
        projects.value.push(r.data[i])
    }
})

async function addNewProject() {
    const r = await request('/project/new', 'POST', {name:'project'}, true)
    showModal.value = true
    nameModal.value = r.data[0].name
    idModal.value = r.data[0].id
}

function openModal(name, id) {
    showModal.value = true
    nameModal.value = name
    idModal.value = id
}

async function closeModal() {
    showModal.value = false
    projects.value = []
    let r = await request('/project/get', 'GET', {}, true)
    for (let i = 0; i < r.data.length; i++) {
        projects.value.push(r.data[i])
    }
}



</script>

<style>
#app{
    align-items: center;
}
</style>

<style scoped>
.content{
    margin-left: 150px;
    margin-top: 20px;
}

.inboxs {
    display: flex;
    flex-direction: column;
    color: var(--gray-color);
    gap: 10px;
}

.inbox {
    display: flex;
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
    margin-top: 100px; 
    width: 100%;
}

.logo {
    display: flex;
    width: 100%; 
    /* height: 100%; */
    margin: 0 auto;
}

.menu {
    position: absolute;
    left: 50px;
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
    padding: 10px;
}

.project:hover{
    background-color: var(--white-color);
    color: var(--black-color);
    outline: 1px solid var(--white-color);
}

input{
    background-color: var(--black-color);
    border: none;
    outline: 1px solid var(--gray-color);
    outline-offset:-1px;

    color: var(--white-color);
    font-family: "Source Code Pro", monospace;
    font-size: 16px;

}

input:hover{
    background-color: var(--white-color);
    color: var(--black-color);
    outline: 1px solid var(--white-color);
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
    }.content {
        margin: 0;
    }
    

}

</style>