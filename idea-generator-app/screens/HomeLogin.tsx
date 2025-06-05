// HomeLogin.tsx (converted to NativeWind)
import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../App';


type NavigationProp = NativeStackNavigationProp<RootStackParamList>;

export default function LoginLandingPage() {
  const navigation = useNavigation<NavigationProp>();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  return (
    <View className="flex-1 justify-center items-center bg-white px-6">
      <View className="w-full items-center mb-10 px-6">
        <Text className="text-3xl font-bold text-black mb-2 text-center">Welcome to</Text>
        <Text className="text-5xl font-extrabold text-black text-center">ProjectForge</Text>
        <Text className="text-base text-gray-500 text-center mt-2">Fuel your creativity. Build your vision.</Text>
      </View>


      <View className="w-full space-y-4">
        <TextInput
          className="w-full bg-gray-100 text-black px-4 py-3 rounded-lg text-base"
          placeholder="Username"
          placeholderTextColor="#999"
          value={username}
          onChangeText={setUsername}
        />
        <TextInput
          className="w-full bg-gray-100 text-black px-4 py-3 rounded-lg text-base"
          placeholder="Password"
          placeholderTextColor="#999"
          secureTextEntry
          value={password}
          onChangeText={setPassword}
        />

        <TouchableOpacity
          className="bg-black py-3 rounded-xl items-center shadow-md"
          onPress={() => navigation.navigate('Dashboard', { firstName })
}
        >
          <Text className="text-white text-lg font-semibold">Login</Text>
        </TouchableOpacity>

        <TouchableOpacity onPress={() => navigation.navigate('SignUp')}>
          <Text className="text-center text-gray-500 underline mt-3">Don't have an account? Sign Up</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}
