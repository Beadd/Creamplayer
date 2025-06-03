import antfu from "@antfu/eslint-config";
import eslintPluginReadableTailwind from "eslint-plugin-readable-tailwind";
import eslintParserVue from "vue-eslint-parser";

export default antfu(
  {
    stylistic: {
      indent: 2, // 4, or 'tab'
      quotes: "double", // or 'single'
      semi: true,
    },
  },
  {
    rules: {
      "style/brace-style": ["error", "1tbs"],
    },
  },
  {
    files: ["**/*.vue"],
    languageOptions: {
      parser: eslintParserVue,
    },
  },
  {
    plugins: {
      "readable-tailwind": eslintPluginReadableTailwind,
    },
    rules: {
      // enable all recommended rules to warn
      ...eslintPluginReadableTailwind.configs.warning.rules,
      // enable all recommended rules to error
      ...eslintPluginReadableTailwind.configs.error.rules,

      // or configure rules individually
      "readable-tailwind/multiline": ["warn", { printWidth: 80 }],
    },
  },
  {
    ignores: ["database.types.ts"],
  },
);
