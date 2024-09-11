<template>
    <div class="container">
        <logo class="logo"></logo>
        <menu-comp sel="tasks" class="menu"></menu-comp>
        <div class="content">
            <div class="titles">
                <div class="title">backlog</div>
                <div class="title">done</div>
                <div class="title">stop</div>
            </div>
            <div class="taskmanager">
                <div class="taskgroup">
                    <div :class="['one-task',{'isdonetask': isdonetask(t), 'isstoptask':isstoptask(t)}]" v-for="(t, i) in today[0]?.tasks?.filter(task => task.status == 'backlog')" :key="i" >
                        {{ t.name }}
                    </div> 
                </div>
                <div class="taskgroup">
                    <div :class="['one-task',{'isdonetask': isdonetask(t), 'isstoptask':isstoptask(t)}]" v-for="(t, i) in today[0]?.tasks?.filter(task => task.status == 'done')" :key="i" >
                        {{ t.name }}
                    </div> 
                </div>
                <div class="taskgroup">
                    <div :class="['one-task',{'isdonetask': isdonetask(t), 'isstoptask':isstoptask(t)}]" v-for="(t, i) in today[0]?.tasks?.filter(task => task.status == 'stop')" :key="i" >
                        {{ t.name }}
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

function isdonetask(task) {
    if (task.status == 'done') {
        return true
    } return false
}

function isstoptask(task) {
    if (task.status == 'stop') {
        return true
    } return false
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

'.'

</script>

<style>
#app{
    align-items: center;
}
</style>

<style scoped lang="scss">
.one-task {
    max-width: 150px;
    overflow: hidden;
    text-overflow: ellipsis;
    position: relative;
    border: var(--gray-color) solid 1px;
    &.isdonetask{
        border: var(--green-color) solid 1px;
        background-color: var(--green-color);
        color: var(--black-color);
    }
    &.isstoptask{
        border: var(--red-color) solid 1px;
    }
}

.title {
    min-width: 150px;
}

.titles{
    display: flex;
    justify-content: space-between;
    max-width: 1000px;
    background-color: var(--white-color);
    color: var(--black-color);
}

.content{
    margin-left: 150px;
}

.one-task{
    max-width: 150px;
}

.taskgroup-title{
    background-color: var(--white-color);
    color: var(--black-color);
}

.taskgroup{
    display: flex;
    flex-direction: column;
    gap: 10px;
    min-width: 150px;
}


.taskmanager{
    display: flex;
    justify-content: space-between;
    max-width: 1000px;
    margin-top: 10px;
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