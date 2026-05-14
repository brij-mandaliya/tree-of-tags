<script setup>
import { ref, defineEmits } from 'vue'

const props = defineProps({
  tree: Array
})

const showChildNode = ref(false)
const emit = defineEmits(['nodeUpdated', 'nodeDeleted'])
const nameEditable = ref(null)
const dataEditable = ref(null)

function collapseNode(id) {
  if (showChildNode.value == id) {
    showChildNode.value = false
  } else {
    showChildNode.value = id
  }
}

function enableNameEdit(id) {
  nameEditable.value = id
}

function enableDataEdit(id) {
  dataEditable.value = id
}

function addChildNode(node) {
  if (!node.children) {
    node.children = []
    delete node.data
  }
  node.children.push({
    id: `${node.id}_${node.children.length + 1}`,
    name: 'New Child',
    data: 'Data',
  })
  
  showChildNode.value = node.id
}

function deleteNode(node) {
  if(typeof node.id === 'string' && node.id.includes("_")) {
    props.tree.splice(props.tree.indexOf(node), 1)
  } else{
    emit('nodeDeleted', node)
  } 
}

function updateNode() {
  if (nameEditable.value) {
    nameEditable.value = null
  }
  if (dataEditable.value) {
    dataEditable.value = null
  }
}

</script>

<template>
  <div v-for="node in tree" :key="node.id" class="bg-blue-200 rounded-xl w-full my-2">

    <div class="flex p-5 items-center ">

      <button
        class="border-2 border-white rounded-full p-2 mr-5 w-10"
        @click="collapseNode(node.id)"
      >
        {{ showChildNode == node.id ? 'v' : '>' }}
      </button>

      <input
        v-model="node.name"
        :readonly="nameEditable !== node.id"
        @click="enableNameEdit(node.id)"
        @blur="updateNode()"
        @keydown.enter="nameEditable = null"
        class="rounded border px-2 py-1 outline-none border-0"
        :class="nameEditable == node.id ? 'bg-white' : ''"
      />

      <div class="ml-auto">
        <button
          @click="addChildNode(node)"
          class="border-2 border-white mx-2 p-2 rounded-md hover:bg-gray-100"
        >
          Add Child
        </button>
        <button
          @click="deleteNode(node)"
          class="border-2 bg-red-400 border-white ml-auto p-2 rounded-md hover:bg-red-600"
        >
          <span class="text-black px-2 py-1 rounded">Remove</span>
        </button>
      </div>

    </div>

    <div
      class="ml-20 pb-10 pr-10"
      v-if="showChildNode == node.id"
    >
      <span v-if="!node.children" class="inline-block mb-2 px-2">
        <span class="rounded">
          Data:
        </span>
        <input
          v-model="node.data"
          :readonly="dataEditable !== node.id"
          @dblclick="enableDataEdit(node.id)"
          @blur="updateNode()"
          @keydown.enter="dataEditable = null"
          class="rounded border px-2 py-1 outline-none border-1 rounded-lg"
          :class="dataEditable == node.id ? 'bg-white' : ''"
        />
      </span>
      <div class="py-2 border border-black/50 rounded-xl" v-if="node.children && node.children.length > 0">
        <TagView :tree="node.children" @nodeUpdated="emit('nodeUpdated', $event)" @nodeDeleted="emit('nodeDeleted', $event)"  />
      </div>
    </div>

  </div>
</template>
