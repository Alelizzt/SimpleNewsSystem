<template>
    <nav>
        <ul>
        <li><RouterLink to="/">Home</RouterLink></li>
        <li><RouterLink to="/login">Login</RouterLink></li>
        <li><RouterLink to="/register">Register</RouterLink></li>
        </ul>
    </nav>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<style>

</style>