import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import type { NativeStackNavigationProp } from '@react-navigation/native-stack';
import type { RootStackParamList } from '../App';
import { useEffect } from 'react';

type NavigationProp = NativeStackNavigationProp<RootStackParamList>;

export default function SignUpScreen() {
  const navigation = useNavigation<NavigationProp>();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [passwordMatchError, setPasswordMatchError] = useState('');

  const allFieldsFilled = firstName && lastName && email && password && confirmPassword;
  const passwordsMatch = password === confirmPassword;
  const isFormValid = allFieldsFilled && passwordsMatch;

    // Update error message when confirmPassword changes
    useEffect(() => {
    if (confirmPassword.length > 0 && !passwordsMatch) {
        setPasswordMatchError("Passwords do not match");
    } else {
        setPasswordMatchError('');
    }
    }, [password, confirmPassword]);

  return (
    <View className="flex-1 bg-white justify-center px-6">
      <Text className="text-2xl font-extrabold text-black text-center mb-8">
        Sign Up With ProjectForge!
      </Text>

      <TextInput
        className="border border-black text-black bg-white p-4 rounded-lg mb-8"
        placeholder="First Name"
        placeholderTextColor="#999"
        value={firstName}
        onChangeText={setFirstName}
      />

      <TextInput
        className="border border-black text-black bg-white p-4 rounded-lg mb-8"
        placeholder="Last Name"
        placeholderTextColor="#999"
        value={lastName}
        onChangeText={setLastName}
      />

      <TextInput
        className="border border-black text-black bg-white p-4 rounded-lg mb-8"
        placeholder="Email"
        placeholderTextColor="#999"
        value={email}
        onChangeText={setEmail}
        autoCorrect={false}
        autoCapitalize="none"
      />
      <TextInput
        className="border border-black text-black bg-white p-4 rounded-lg mb-8"
        placeholder="Password"
        placeholderTextColor="#999"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
        textContentType="none"
        autoComplete="off"
        autoCorrect={false}
        spellCheck={false}
      />
      <TextInput
        className="border border-black text-black bg-white p-4 rounded-lg mb-4"
        placeholder="Confirm Password"
        placeholderTextColor="#999"
        secureTextEntry
        value={confirmPassword}
        onChangeText={setConfirmPassword}
        textContentType="none"
        autoComplete="off"
        autoCorrect={false}
        spellCheck={false}
      />
      {passwordMatchError !== '' && (
        <Text className="text-red-500 mb-4 text-sm text-center">{passwordMatchError}</Text>
        )}

      <TouchableOpacity onPress={() => navigation.navigate('Dashboard')} className={`py-4 rounded-xl items-center mb-4 ${isFormValid ? 'bg-black' : 'bg-gray-400'}`} disabled={!isFormValid}>
         <Text className="text-white text-lg font-semibold">Create Account</Text>
        </TouchableOpacity>

      <TouchableOpacity onPress={() => navigation.navigate('HomeLogin')}>
        <Text className="text-center text-gray-500 underline mt-3">
          Back to Home
        </Text>
      </TouchableOpacity>
    </View>
  );
}
