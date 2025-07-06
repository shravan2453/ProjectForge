import React, { useState, useRef } from 'react';
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
  const [formFocused, setFormFocused] = useState(false);
  const focusedInputs = useRef(0);

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

  // Handlers to track focus/blur across all inputs
  const handleInputFocus = () => {
    focusedInputs.current += 1;
    setFormFocused(true);
  };
  const handleInputBlur = () => {
    focusedInputs.current -= 1;
    if (focusedInputs.current <= 0) {
      setFormFocused(false);
      focusedInputs.current = 0;
    }
  };

  return (
    <View
      className="flex-1 bg-white px-6"
      style={{ justifyContent: formFocused ? 'flex-start' : 'center', paddingTop: formFocused ? 60 : 0 }}
    >
      <Text className="text-2xl font-extrabold  text-center mb-8" style={{ fontFamily: 'Klados-Bold' }}>
        Sign Up With Klados
      </Text>

      <TextInput
        className={`border border-black text-black bg-white p-4 rounded-lg mb-3`}
        placeholder="First Name"
        placeholderTextColor="#999"
        value={firstName}
        onChangeText={setFirstName}
        onFocus={handleInputFocus}
        onBlur={handleInputBlur}
      />

      <TextInput
        className={`border border-black text-black bg-white p-4 rounded-lg mb-3`}
        placeholder="Last Name"
        placeholderTextColor="#999"
        value={lastName}
        onChangeText={setLastName}
        onFocus={handleInputFocus}
        onBlur={handleInputBlur}
      />

      <TextInput
        className={`border border-black text-black bg-white p-4 rounded-lg mb-3`}
        placeholder="Email"
        placeholderTextColor="#999"
        value={email}
        onChangeText={setEmail}
        autoCorrect={false}
        autoCapitalize="none"
        onFocus={handleInputFocus}
        onBlur={handleInputBlur}
      />
      <TextInput
        className={`border border-black text-black bg-white p-4 rounded-lg mb-3`}
        placeholder="Password"
        placeholderTextColor="#999"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
        textContentType="none"
        autoComplete="off"
        autoCorrect={false}
        spellCheck={false}
        onFocus={handleInputFocus}
        onBlur={handleInputBlur}
      />
      <TextInput
        className={`border border-black text-black bg-white p-4 rounded-lg mb-6`}
        placeholder="Confirm Password"
        placeholderTextColor="#999"
        secureTextEntry
        value={confirmPassword}
        onChangeText={setConfirmPassword}
        textContentType="none"
        autoComplete="off"
        autoCorrect={false}
        spellCheck={false}
        onFocus={handleInputFocus}
        onBlur={handleInputBlur}
      />
      {passwordMatchError !== '' && (
        <Text className={`text-red-500 ${formFocused ? 'mb-3' : 'mb-4'} text-sm text-center`}>{passwordMatchError}</Text>
        )}

      <TouchableOpacity onPress={() => navigation.navigate('Dashboard')} className={`py-4 rounded-xl items-center ${formFocused ? 'mb-3' : 'mb-4'} ${isFormValid ? 'bg-black' : 'bg-gray-400'}`} disabled={!isFormValid}>
         <Text className="text-white text-lg" style={{ fontFamily: 'Klados-Bold' }}>Create Account</Text>
        </TouchableOpacity>

      <TouchableOpacity onPress={() => navigation.navigate('HomeLogin')}>
        <Text className="text-center text-gray-500 underline mt-3" style={{ fontFamily: 'Klados-Bold' }}>
          Back to Home
        </Text>
      </TouchableOpacity>
    </View>
  );
}
