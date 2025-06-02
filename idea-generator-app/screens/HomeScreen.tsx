import React, { useState } from 'react';
import {
  View,
  TextInput,
  Button,
  StyleSheet,
  Text,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../App';
import { Pressable } from 'react-native';
import CustomHeader from '../screens/CustomHeader';




type Props = NativeStackScreenProps<RootStackParamList, 'Home'>;

export default function HomeScreen({ navigation }: Props) {
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
    
    <ScrollView contentContainerStyle={styles.container}>
      <CustomHeader title="ProjectForge" />
      <Text style={styles.header}>Welcome to ProjectForge</Text>
      <Text style={styles.subheader}>Let’s build your next big idea!</Text>
      {Object.entries(form).map(([key, value]) => (
        <View key={key} style={styles.inputGroup}>
            <Text style={styles.label}>{labelsAndPlaceholders[key].label}</Text>
            <TextInput
            style={styles.input}
            value={value}
            onChangeText={(text) => handleChange(key, text)}
            placeholder={labelsAndPlaceholders[key].placeholder}
            placeholderTextColor="#999"
            />
        </View>
        ))}


      
    <Pressable
        style={({ pressed }) => [
            styles.button,
            !allFieldsFilled && styles.buttonDisabled,
            pressed && { opacity: 0.8 },
        ]}
        disabled={!allFieldsFilled}
        onPress={handleSubmit}
        >
        <Text style={styles.buttonText}>Generate Ideas</Text>
    </Pressable>

    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 24,
    backgroundColor: '#ffffff',
    flexGrow: 1,
  },
  header: {
    fontSize: 30,
    fontFamily: 'Inter-SemiBold',
    marginBottom: 8,
    color: '#111',
  },
  subheader: {
    fontSize: 16,
    fontFamily: 'Inter',
    marginBottom: 25,
    color: '#666',
  },
  inputGroup: {
    marginBottom: 24,
  },
  label: {
    fontFamily: 'Inter-Medium',
    fontSize: 14,
    marginBottom: 6,
    color: '#333',
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    padding: 14,
    borderRadius: 10,
    fontSize: 16,
    fontFamily: 'Inter',
    color: '#000',
    backgroundColor: '#fafafa',
  },
  button: {
    marginTop: 10,
    backgroundColor: '#111',
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  buttonDisabled: {
    backgroundColor: '#ccc',
  },
  buttonText: {
    color: '#fff',
    fontFamily: 'Inter-Bold',
    fontSize: 16,
  },
});
