<template>
    <div class="menu">
        <router-link to="overview" class="el overview">overview</router-link>
        <router-link to="inbox" class="el inbox">inbox</router-link>
        <router-link to="tasks" class="el tasks">tasks</router-link>
        <router-link to="projects" class="el projects">projects</router-link>
        <router-link to="settings" class="el settings">settings</router-link>
    </div>
</template>

<script>
import { RouterLink } from 'vue-router';
import { onMounted } from 'vue';
export default {
    props: {
        sel: {
            type: String,
            required: true
        }
    },
    setup(props) {
        onMounted(()=> {
            document.querySelector(`.${props.sel}`).classList.add('sel')
        })
    }
} 
</script>


<style scoped>
    .menu{
        display: flex;
        flex-direction: column;
        gap: 20px;
        color: var(--gray-color);
    }
    
    a{
        color: var(--gray-color);
        text-decoration: none;
    }
    .sel {
        background-color: var(--gray-color);
        color: var(--black-color);
    }
    
    .el:hover {
        background-color: var(--gray-color);
        color: var(--black-color);
        }

    .sel:hover{
        background-color: var(--black-color);
        color: var(--gray-color);
    }


</style>