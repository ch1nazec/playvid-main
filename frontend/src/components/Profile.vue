<template>
<div class="container py-5">
    <h2 class="mb-4">Личный кабинет</h2>
    
    <div class="row">
        <!-- Левая колонка: Аватар и навигация -->
        <div class="col-lg-4 mb-4">
            <div class="card shadow-sm">
                <div class="card-body text-center">
                    <img src="https://via.placeholder.com/150" alt="Аватар" class="rounded-circle img-fluid mb-3" style="width: 150px; height: 150px;">
                    <h5>Иван Иванов</h5>
                    <p class="text-muted">ivan@example.com</p>
                    <button class="btn btn-outline-primary btn-sm">Изменить фото</button>
                </div>
            </div>
        </div>

        <!-- Правая колонка: Данные формы -->
        <div class="col-lg-8">
            <div class="card shadow-sm">
                <div class="card-body">
                    <h5 class="card-title mb-4">Основные данные</h5>
                    <form>
                        <div class="row mb-3">
                            <div class="col-md-6">
                                <label class="form-label">Имя</label>
                                <input type="text" class="form-control" value="Иван">
                            </div>
                            <div class="col-md-6">
                                <label class="form-label">Фамилия</label>
                                <input type="text" class="form-control" value="Иванов">
                            </div>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Email</label>
                            <input type="email" class="form-control" value="ivan@example.com">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Телефон</label>
                            <input type="tel" class="form-control" value="+7 (900) 000-00-00">
                        </div>
                        <button type="submit" class="btn btn-primary">Сохранить изменения</button>
                    </form>
                </div>
            </div>

            <!-- Блок безопасности -->
            <div class="card shadow-sm mt-4">
                <div class="card-body">
                    <h5 class="card-title mb-3">Безопасность</h5>
                    <button class="btn btn-outline-danger btn-sm">Сменить пароль</button>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script setup>
import {useAuthStore} from '@/stores/auth'
import { useUserDetail } from '@/stores/user';
import { ref, computed, onMounted } from 'vue';

const user = computed(() => userStore.user);
const userStore = useAuthStore();

onMounted(async () => {
    await userStore.fetchUser()})
</script>

<style>
.simple-profile {
  max-width: 500px;
  margin: 30px auto;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

h3 {
  margin-top: 0;
  color: #333;
  border-bottom: 2px solid #667eea;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.field {
  margin: 15px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.field:last-child {
  border-bottom: none;
}

label {
  font-weight: 600;
  color: #555;
  min-width: 100px;
}

span {
  color: #333;
  text-align: right;
  flex: 1;
}

.username {
  color: #667eea;
  font-weight: 500;
}
</style>