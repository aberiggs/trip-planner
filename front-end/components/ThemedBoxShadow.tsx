import { View, type ViewProps, StyleSheet } from "react-native";

import { useThemeColor, ColorTypes } from "@/hooks/useThemeColor";

export type ThemedBoxShadowProps = ViewProps & {
  lightShadowColor?: string;
  darkShadowColor?: string;
  shadowColor?: ColorTypes;
};

export function ThemedBoxShadow({
  style,
  lightShadowColor,
  darkShadowColor,
  shadowColor = ColorTypes.primary,
  ...rest
}: ThemedBoxShadowProps) {
  const themedShadowColor = useThemeColor(
    { light: lightShadowColor, dark: darkShadowColor },
    shadowColor
  );

  return (
    <View
      style={[
        styles.boxShadow,
        style,
        {
          shadowColor: themedShadowColor,
        },
      ]}
      {...rest}
    />
  );
}

const styles = StyleSheet.create({
  boxShadow: {
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
});
