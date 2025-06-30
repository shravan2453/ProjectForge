import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../App';

type NavigationProp = NativeStackNavigationProp<RootStackParamList>;




type Props = {
  title: string;
  showBack?: boolean;
};

export default function CustomHeader({ title, showBack = false }: Props) {
  const navigation = useNavigation<NavigationProp>(); // ✅ typed navigation

  return (
    <View className="pt-12 pb-4 px-5 bg-white flex-row justify-between items-center border-b border-gray-200 mt-2">
      {showBack ? (
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Text className="text-blue-500 text-base font-medium">← Back</Text>
        </TouchableOpacity>
      ) : (
        <View className="w-[50px]" /> // layout placeholder
      )}

      <Text className="text-xl font-bold text-black text-center" style={{ fontFamily: 'Klados-Bold' }}>{title}</Text>
      {showBack ? (
          <View className="w-[50px]" />
        ) : (
          <TouchableOpacity onPress={() => navigation.navigate('HomeLogin')}>
            <Text className="text-gray-600 text-sm underline font-medium" style={{ fontFamily: 'Klados-Bold' }}>Log Out</Text>
          </TouchableOpacity>
        )}

    </View>
  );
}
