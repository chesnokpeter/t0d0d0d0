<template>
    <div class="container">
        <logo class="logo"></logo>
        <menu-comp sel="tasks" class="menu"></menu-comp>
        <div class="content">
            <div class="taskmanager">
                <div class="taskgroup backlog-manager">
                    <div class="taskgroup-title">backlog</div>
                    <div class="backlog" v-for="(t, i) in today[0].tasks" :key="i" >
                        <div class="backlog-task" v-if="t.status == 'backlog'">{{ t.name }}</div>
                    </div> 
                </div>
                <div class="taskgroup done-manager">
                    <div class="taskgroup-title">done</div>
                    <div class="done" v-for="(t, i) in today[0].tasks" :key="i" >
                        <div class="done-task" v-if="t.status == 'done'">{{ t.name }}</div>
                    </div> 
                </div>
                <div class="taskgroup stop-manager">
                    <div class="taskgroup-title">stop</div>
                    <div class="stop" v-for="(t, i) in today[0].tasks" :key="i" >
                        <div class="stop-task" v-if="t.status == 'stop'">{{ t.name }}</div>
                    </div> 
                </div>
            </div>
        </div>
    </div>

</template>


<script setup>
import Logo from '../components/Logo.vue'
import { request } from '@/modules/requester'
import MenuComp from '../components/MenuComp.vue'
import { onMounted, ref } from 'vue';
import { calday } from '@/modules/calday'

const today = ref([new calday(todaydate())])

function todaydate() {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`
}


async function gettasksbydate(date) {
    let r = await request('/task/get/byDate', 'POST', {date:date}, true)
    if (Object.keys(r.data[0]).length === 0) {
        return []
    }
    return r.data
}

onMounted(async ()=> {
    let t = await gettasksbydate(today.value[0].y_m_d())
    today.value[0].setTasks(t)
    console.log(today);
    
})


</script>

<style>
#app{
    align-items: center;
}
</style>

<style scoped>
.content{
    margin-left: 150px;
    /* margin-top: 20px; */
}

.taskgroup-title{
    background-color: var(--white-color);
    color: var(--black-color);
}


.taskmanager{
    display: flex;
    justify-content: space-between;
}

.menu {
    position: absolute;
    left: 50px;
}

.container {
    position: relative;
    margin-top: 100px; 
    width: 100%;
}

.logo {
    display: flex;
    width: 100%; 
    margin: 0 auto;
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