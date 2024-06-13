import { Pressable, type PressableProps, ViewStyle, PressableStateCallbackType, StyleProp } from 'react-native';
import { useCallback } from 'react';

import { useThemeColor } from '@/hooks/useThemeColor';

export type ThemedPressableProps = PressableProps & {
  lightColor?: string;
  darkColor?: string;
};

export function ThemedButton({ style, lightColor, darkColor, ...otherProps }: ThemedPressableProps) {
  const backgroundColor = useThemeColor({ light: lightColor, dark: darkColor }, 'text');

  // style is either a ViewStyle or a function that returns a ViewStyle :)
  const getStyle = useCallback((state: PressableStateCallbackType): StyleProp<ViewStyle> => {
    const incomingStyle = typeof style === "function" ? style(state) : style;
    return [
      {borderRadius: 5, padding: 10, margin: 10},
      {backgroundColor: state.pressed ? 'white' : backgroundColor},
      incomingStyle,
    ]
  }, [style])

  // Return a pressable with the set background color and text color
  return (
    <Pressable
      style={getStyle}
      {...otherProps}
    />
  );

}

