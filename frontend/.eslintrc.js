module.exports = {
  root: true,
  extends: [
    'plugin:vue/vue3-essential',
    'eslint:recommended'
  ],
  rules: {
    'vue/multi-word-component-names': 'off',
    'vue/valid-template-root': 'off',
    'no-undef': 'off',
    // 'no-unused-vars': 'off'
    'vue/valid-define-props': 'off',
    'vue/valid-define-emits': 'off'
  }
}