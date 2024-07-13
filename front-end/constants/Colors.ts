/**
 * Below are the colors that are used in the app. The colors are defined in the light and dark mode.
 * There are many other ways to style your app. For example, [Nativewind](https://www.nativewind.dev/), [Tamagui](https://tamagui.dev/), [unistyles](https://reactnativeunistyles.vercel.app), etc.
 */

const tintColorLight = "#0a7ea4";
const tintColorDark = "#fff";

export enum ColorTypes {
  base = "base", // Base color - "background color"
  primary = "primary",
  secondary = "secondary",
  transparent = "transparent",
  input = "input",
}

export const Colors = {
  light: {
    base: "#fff",
    primary: "#11181C",
    secondary: "#656565",
    input: "#F7F7F7",
    info: "#0a7ea4",
  },
  dark: {
    base: "#16161d",
    // #4A4E69
    // #9A8C98
    primary: "#F2E9E4",
    secondary: "#A6A09C",
    input: "#2A2A2A",
    info: "#C9ADA7",
  },
  transparent: "transparent",
};
