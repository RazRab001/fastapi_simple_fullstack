<template>
  <div id="app">
    <h1>Favorite Movies</h1>

    <form @submit.prevent="addMovie">
      <input v-model="userName" placeholder="Your Name" />
      <input v-model="movieTitle" placeholder="Favorite Movie" />
      <button type="submit">Add Movie</button>
    </form>

    <h2>Movies List</h2>
    <ul>
      <li v-for="movie in movies" :key="movie.id">{{ movie.title }} (added by user with ID: {{ movie.owner_id }})</li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userName: '',
      movieTitle: '',
      movies: []
    }
  },
  mounted() {
    this.fetchMovies();
  },
  methods: {
    async fetchMovies() {
      try {
        const response = await fetch('/api/movies/');  // Теперь используем /api для проксирования
        this.movies = await response.json();
      } catch (error) {
        console.error('Failed to fetch movies:', error);
      }
    },
    async addMovie() {
      try {
        let user = await fetch('/api/users/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: this.userName })
        }).then(res => res.json());
        await fetch(`/api/users/${user.id}/movies/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title: this.movieTitle })
        });

        this.fetchMovies();

        this.userName = '';
        this.movieTitle = '';
      } catch (error) {
        console.error('Failed to add movie:', error);
      }
    }
  }
}
</script>

<style>
#app {
  text-align: center;
}
form {
  margin-bottom: 20px;
}
</style>

