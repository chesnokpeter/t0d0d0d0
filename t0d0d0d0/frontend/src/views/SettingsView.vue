<template>
    <div class="container">
        <logo class="logo"></logo>
        <menu-comp sel="settings" class="menu"></menu-comp>
        <div class="content">

            <div class="bot">
                <div class="type">client</div>
                <div class="name">telegram bot</div>
                <div class="mode">linked</div>
                <div class="integration">@</div>
            </div>

        </div>
    </div>


</template>


<script setup>
import Logo from '../components/Logo.vue'
import MenuComp from '../components/MenuComp.vue'



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