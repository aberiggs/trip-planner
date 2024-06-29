/**
 * Learn more about light and dark modes:
 * https://docs.expo.dev/guides/color-schemes/
 */

import { useColorScheme } from 'react-native';

import { Colors, ColorTypes } from '@/constants/Colors';
 
export function useThemeColor(
  props: { light?: string; dark?: string },
  colorName: ColorTypes
) {
  const theme = useColorScheme() ?? 'light';
  const colorFromProps = props[theme];

  if (colorName === 'transparent') {
    return 'transparent';
  }

  if (colorFromProps) {
    return colorFromProps;
  } else {
    return Colors[theme][colorName];
  }
}

// Export the ColorTypes for anywhere that wants to use the color themes hook
export { ColorTypes } from '@/constants/Colors';