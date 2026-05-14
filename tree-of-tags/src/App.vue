<script setup>
import { onMounted, reactive } from 'vue';
import TagView from './components/TagView.vue';

const data = reactive([])

async function fetchData() {
  const res = await fetch('http://localhost:8002/api/trees/')
  data.value = await res.json()
  console.log("data", data.value)
}

async function addNode() {
  const node = { name: 'New Node', data: 'Data' }

  await fetch('http://localhost:8002/api/trees/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      json: node
    })
  }).then(() => {
    fetchData()
  })
}

onMounted(() => {
  fetchData()
})

async function handleNodeUpdated(node) {

  const json = {
    name: node.name
  }

  if (node.hasOwnProperty('data')) {
    json.data = node.data
  }  else {
    json.children = node.children
  }

  await fetch(`http://localhost:8002/api/trees/${node.id}/`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      json: json
    })
  })
}

async function handleNodeDeleted(node) {
  await fetch(`http://localhost:8002/api/trees/${node.id}/`, {
    method: 'DELETE'
  }).then(() => {
    fetchData()
  })
}

async function updateData() {
  data.value.forEach(node => {
    handleNodeUpdated(node)
  })
  
  setTimeout(() => {
    fetchData()
  }, 2000)
}





</script>

<template>
  <div class="min-h-screen">
    <div class="bg-gray-100 h-150 border-1 rounded-lg m-10 overflow-y-scroll">
      <div class="flex px-10  py-5">
        <button class="ml-auto bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg" @click="addNode"> Add Node + </button>
      </div>
      <div class="w-full p-5">
        <TagView :tree="data.value" @nodeDeleted="handleNodeDeleted" />
      </div>
    </div>
    <div class="m-10">
      <button class="p-2 border-2 border-blue-600 text-sky-600 hover:bg-blue-300 hover:text-white font-bold rounded-md" @click="updateData()"> Export </button>
      <pre class="bg-black text-white p-4 rounded mt-5">
        {{ 
          JSON.stringify(
            data.value,
            (key, value) => {
              if ( value && typeof value === 'object' && value.is_deleted) {
                return undefined
              }
              if (key === 'id' || key === 'updated_at' || key === 'created_at') {
                return undefined
              }
              return value
            },
            2
          )
        }}
      </pre>
    </div>
  </div>
</template>
