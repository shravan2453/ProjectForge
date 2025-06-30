// FormScreen.tsx (Converted to NativeWind)
import React, { useState } from 'react';
import { View, TextInput, Text, ScrollView, TouchableOpacity, Pressable } from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../App';
import CustomHeader from './CustomHeader';


type Props = NativeStackScreenProps<RootStackParamList, 'Form'>;

export default function FormScreen({ navigation }: Props) {
  const [form, setForm] = useState({
    project_type: '',
    project_interest: '',
    project_technical: '',
    project_potential: '',
    project_additional: '',
  });

  const handleChange = (key: string, value: string) => {
    setForm({ ...form, [key]: value });
  };

  const allFieldsFilled = Object.values(form).every((val) => val.trim() !== '');

  const handleSubmit = () => {
    if (allFieldsFilled) {
      navigation.navigate('Ideas', { formData: form });
    }
  };

  const labelsAndPlaceholders: Record<string, { label: string; placeholder: string }> = {
    project_type: {
      label: 'What is this project for?',
      placeholder: 'e.g. Hackathon, Startup, School, Personal Portfolio...',
    },
    project_interest: {
      label: 'What topic are you interested in?',
      placeholder: 'e.g. Sports, Law, Education, Aviation...',
    },
    project_technical: {
      label: 'What technical skills do you want to use?',
      placeholder: 'e.g. Machine Learning, AI, React, No Code, None...',
    },
    project_potential: {
      label: 'Do you have a rough idea of your project already?',
      placeholder: 'e.g. Something related to analyzing sports stats...',
    },
    project_additional: {
      label: 'Anything else we should consider?',
      placeholder: 'e.g. You’re working with 2 friends, want to avoid web apps...',
    },
  };

  return (
    <ScrollView contentContainerStyle={{ flexGrow: 1 }} className="bg-white px-6 py-4">
      <CustomHeader title="Klados AI" showBack={false} />

      <Text className="mt-4 text-3xl font-semibold text-black mb-2 text-center" style={{ fontFamily: 'Klados-Bold' }}>Welcome to Klados</Text>
      <Text className="text-base text-gray-500 mb-6 justify-center text-center" style={{ fontFamily: 'Klados-Italic' }}>Let’s Build Your Next Big Idea.</Text>

      {Object.entries(form).map(([key, value]) => (
        <View key={key} className="mb-6">
          <Text className="mt-0 text-sm font-medium text-gray-800 mb-1">
            {labelsAndPlaceholders[key].label}
          </Text>
          <TextInput
            className="border border-gray-300 bg-gray-100 text-black rounded-lg p-4 text-base"
            value={value}
            onChangeText={(text) => handleChange(key, text)}
            placeholder={labelsAndPlaceholders[key].placeholder}
            placeholderTextColor="#999"
          />
        </View>
      ))}

      <Pressable
        className={`-mt-1 -mb-3 py-4 rounded-xl items-center ${allFieldsFilled ? 'bg-black' : 'bg-gray-400'}`}
        disabled={!allFieldsFilled}
        onPress={handleSubmit}
      >
        <Text className="text-white text-base font-bold" style={{ fontFamily: 'Klados-Bold' }}>Generate Ideas</Text>
      </Pressable>

      <TouchableOpacity
        className="mt-4 py-3 items-center"
        onPress={() => navigation.navigate('Dashboard')}
      >
        <Text className="text-gray-600 text-sm underline font-medium" style={{ fontFamily: 'Klados-Bold' }}>Back to Dashboard</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}