// HomeLogin.tsx (converted to NativeWind)
import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, Image } from 'react-native';
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
        <Image
          source={require('../images/klados.png')}
          style={{ width: 325, height: 325, resizeMode: 'contain' }}
          className="-mb-2 -mt-6"     
        />
        <Text className="text-black text-center -mt-4" style={{ fontSize: 18, fontFamily: 'Klados-Italic' }}>Don’t know where to start?</Text>
        <Text className="text-black text-center mt-0 -mb-0" style={{ fontSize: 18, fontFamily: 'Klados-Italic' }} >Start Here.</Text>
      </View>


      <View className="w-full space-y-4">
        <TextInput
          className="w-full bg-gray-100 text-black px-4 py-3 rounded-lg text-base mb-4" style={{ fontFamily: 'Klados-Main' }}
          placeholder="Username"
          placeholderTextColor="#999"
          value={username}
          onChangeText={setUsername}
        />
        <TextInput
          className="w-full bg-gray-100 text-black px-4 py-3 rounded-lg text-base mb-6" style={{ fontFamily: 'Klados-Main' }}
          placeholder="Password"
          placeholderTextColor="#999"
          secureTextEntry
          value={password}
          onChangeText={setPassword}
        />

        <TouchableOpacity
          className="bg-black py-3 rounded-xl items-center shadow-md mt-6"
          onPress={() => navigation.navigate('Dashboard')}
        >
          <Text className="text-white text-lg font-semibold" style={{ fontFamily: 'Klados-Bold' }}>Login</Text>
        </TouchableOpacity>

        <TouchableOpacity onPress={() => navigation.navigate('SignUp')}>
          <Text className="text-center text-gray-600 underline mt-4" style={{ fontFamily: 'Klados-Main' }}>Don't have an account? Sign Up</Text>
          
        </TouchableOpacity>
      </View>
    </View>
  );
}
