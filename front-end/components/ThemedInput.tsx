import { Text, type TextInputProps, StyleSheet, TextInput } from "react-native";

import { useThemeColor, ColorTypes } from "@/hooks/useThemeColor";

export type ThemedInputProps = TextInputProps & {
  lightBorderColor?: string;
  darkBorderColor?: string;
  borderColor?: ColorTypes;

  lightBgColor?: string;
  darkBgColor?: string;
  bgColor?: ColorTypes;

  lightPlaceholderTextColor?: string;
  darkPlaceholderTextColor?: string;
  placeholderTextColor?: ColorTypes;

  lightTextColor?: string;
  darkTextColor?: string;
  textColor?: ColorTypes;

  lightShadowColor?: string;
  darkShadowColor?: string;
  shadowColor?: ColorTypes;
};

export function ThemedInput({
  style,
  lightBorderColor,
  darkBorderColor,
  borderColor = ColorTypes.input,
  lightBgColor,
  darkBgColor,
  bgColor = ColorTypes.input,
  lightPlaceholderTextColor,
  darkPlaceholderTextColor,
  placeholderTextColor = ColorTypes.secondary,
  lightTextColor,
  darkTextColor,
  textColor = ColorTypes.primary,
  ...rest
}: ThemedInputProps) {
  const themedPlaceholderColor = useThemeColor(
    { light: lightPlaceholderTextColor, dark: darkPlaceholderTextColor },
    placeholderTextColor
  );

  const themedBgColor = useThemeColor(
    { light: lightBgColor, dark: darkBgColor },
    bgColor
  );

  const themedBorderColor = useThemeColor(
    { light: lightBgColor, dark: darkBgColor },
    bgColor
  );

  const themedTextColor = useThemeColor(
    { light: lightTextColor, dark: darkTextColor },
    textColor
  );

  return (
    <TextInput
      style={[
        styles.input,
        style,
        {
          borderColor: themedBorderColor,
          backgroundColor: themedBgColor,
          color: themedTextColor,
        },
      ]}
      placeholderTextColor={themedPlaceholderColor}
      {...rest}
    />
  );
}

const styles = StyleSheet.create({
  input: {
    height: 45,
    borderWidth: 1,
    width: 300,
    paddingHorizontal: 10,
    borderRadius: 5,
  },
});
