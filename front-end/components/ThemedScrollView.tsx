import { ScrollView, type ScrollViewProps } from 'react-native';

import { useThemeColor, ColorTypes } from '@/hooks/useThemeColor';

export type ThemedScrollViewProps = ScrollViewProps & {
  lightColor?: string;
  darkColor?: string;
  color: ColorTypes;
};

export function ThemedScrollView({ style, lightColor, darkColor, color = ColorTypes.base, ...otherProps }: ThemedScrollViewProps) {
  const backgroundColor = useThemeColor({ light: lightColor, dark: darkColor }, color);

  return <ScrollView style={[{ backgroundColor }, style]} {...otherProps} />;
}
