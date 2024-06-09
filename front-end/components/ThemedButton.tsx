import { Pressable, type PressableProps } from 'react-native';

import { useThemeColor } from '@/hooks/useThemeColor';

export type ThemedPressableProps = PressableProps & {
  lightColor?: string;
  darkColor?: string;
};

export function ThemedButton({ style, lightColor, darkColor, ...otherProps }: ThemedPressableProps) {
  const backgroundColor = useThemeColor({ light: lightColor, dark: darkColor }, 'text');
  const textColor = useThemeColor({ light: lightColor, dark: darkColor }, 'background');

  // Return a pressable with the set background color and text color
  return <Pressable style={[{ backgroundColor, color: textColor }, style]} {...otherProps} />;

}

