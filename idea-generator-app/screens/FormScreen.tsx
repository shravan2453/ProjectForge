// FormScreen.tsx (Converted to NativeWind)
import React, { useState, useRef, useEffect } from 'react';
import { View, TextInput, Text, ScrollView, TouchableOpacity, Pressable, Keyboard, Alert, KeyboardAvoidingView, Platform, Animated } from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../App';
import CustomHeader from './CustomHeader';
import * as DocumentPicker from 'expo-document-picker';

type Props = NativeStackScreenProps<RootStackParamList, 'Form'>;

export default function FormScreen({ navigation }: Props) {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [form, setForm] = useState({
    project_type: '',
    project_interest: '',
    project_technical: '',
    project_potential: '',
    project_additional: '',
  });
  const [uploadedDocument, setUploadedDocument] = useState<{
    name: string;
    content: string;
  } | null>(null);

  const inputRef = useRef<TextInput>(null);
  const progressAnim = useRef(new Animated.Value(0)).current;

  const questions = [
    {
      key: 'project_type',
      label: 'What is this project for?',
      placeholder: 'e.g. Hackathon, Startup, School, Personal Portfolio...',
    },
    {
      key: 'project_interest',
      label: 'What topic are you interested in?',
      placeholder: 'e.g. Sports, Law, Education, Aviation...',
    },
    {
      key: 'project_technical',
      label: 'What technical skills do you want to use?',
      placeholder: 'e.g. Machine Learning, AI, React, No Code, None...',
    },
    {
      key: 'project_potential',
      label: 'Do you have a rough idea of your project already?',
      placeholder: 'e.g. Something related to analyzing sports stats...',
    },
    {
      key: 'project_additional',
      label: 'Anything else we should consider? (Optional: Upload guidelines/instructions)',
      placeholder: 'e.g. You\'re working with 2 friends, want to avoid web apps...',
      hasFileUpload: true,
    },
  ];

  const currentQuestion = questions[currentQuestionIndex];

  useEffect(() => {
    // Auto-focus the input when question changes
    setTimeout(() => {
      inputRef.current?.focus();
    }, 100);
  }, [currentQuestionIndex]);

  useEffect(() => {
    // Animate progress bar when question changes
    const targetProgress = (currentQuestionIndex / questions.length) * 100;
    Animated.timing(progressAnim, {
      toValue: targetProgress,
      duration: 500,
      useNativeDriver: false,
    }).start();
  }, [currentQuestionIndex, questions.length]);

  const handleChange = (key: string, value: string) => {
    setForm({ ...form, [key]: value });
  };

  const handleDocumentPick = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: ['application/pdf', 'text/plain', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
        copyToCacheDirectory: true,
      });

      if (result.canceled) {
        return;
      }

      const file = result.assets[0];

      // For now, we'll just store the file info
      // In a real app, you'd want to read the file content here
      setUploadedDocument({
        name: file.name,
        content: `Document: ${file.name} (${file.size} bytes)`, // Placeholder content
      });

      Alert.alert('Success', `Document "${file.name}" uploaded successfully!`);
    } catch (error) {
      console.error('Error picking document:', error);
      Alert.alert('Error', 'Failed to upload document. Please try again.');
    }
  };

  const handleNext = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      // All questions completed, navigate to Ideas
      
      // Ensure all fields are filled
      const allFieldsFilled = Object.values(form).every((val) => val.trim() !== '');
      if (allFieldsFilled) {
        navigation.navigate('Ideas', { 
          formData: form,
          uploadedDocument: uploadedDocument 
        });
      } else {
        console.error('Not all fields are filled:', form);
      }
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const handleSubmitEditing = () => {
    Keyboard.dismiss();
    handleNext();
  };

  const isLastQuestion = currentQuestionIndex === questions.length - 1;
  const canProceed = form[currentQuestion.key as keyof typeof form].trim() !== '';

  return (
    <KeyboardAvoidingView 
      className="flex-1 bg-white"
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 20}
    >
      <CustomHeader title="Klados AI" showBack={false} />

      {/* Progress Indicator */}
      <View className="px-6 py-3">
        <View className="flex-row justify-between items-center mb-3">
          <Text className="text-sm text-gray-500" style={{ fontFamily: 'Klados-Bold' }}>
            Question {currentQuestionIndex + 1} of {questions.length}
          </Text>
          <Animated.Text 
            className="text-sm text-gray-500" 
            style={{ 
              fontFamily: 'Klados-Bold',
              opacity: progressAnim.interpolate({
                inputRange: [0, 100],
                outputRange: [0.7, 1],
              })
            }}
          >
            {Math.round((currentQuestionIndex / questions.length) * 100)}%
          </Animated.Text>
        </View>
        <View className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
          <Animated.View 
            className="bg-black rounded-full h-3" 
            style={{ 
              width: progressAnim.interpolate({
                inputRange: [0, 100],
                outputRange: ['0%', '100%'],
              }),
              shadowColor: '#000',
              shadowOffset: { width: 0, height: 1 },
              shadowOpacity: 0.3,
              shadowRadius: 3,
              elevation: 3
            }}
          />
        </View>
      </View>

      {/* Current Question */}
      <View className="flex-1 px-6 justify-start pt-4">
        <Text className="text-xl font-semibold text-black mb-4 text-center" style={{ fontFamily: 'Klados-Bold' }}>
          {currentQuestion.label}
        </Text>
        
        {/* File Upload Section for Last Question */}
        {currentQuestion.hasFileUpload ? (
          <View className="mb-4">
            {/* Horizontal split: Text input (80%) + Upload button (20%) */}
            <View className="flex-row items-center space-x-3">
              <View className="flex-1">
                <TextInput
                  ref={inputRef}
                  className="border border-gray-300 bg-gray-100 text-black rounded-lg p-4 text-base"
                  value={form[currentQuestion.key as keyof typeof form]}
                  onChangeText={(text) => handleChange(currentQuestion.key, text)}
                  placeholder={currentQuestion.placeholder}
                  placeholderTextColor="#999"
                  onSubmitEditing={handleSubmitEditing}
                  returnKeyType={isLastQuestion ? "done" : "next"}
                  blurOnSubmit={false}
                  multiline={true}
                  numberOfLines={3}
                />
              </View>
              
              <TouchableOpacity
                className="w-20 h-20 border-2 border-dashed border-gray-300 rounded-lg items-center justify-center bg-gray-50"
                onPress={handleDocumentPick}
              >
                <Text className="text-gray-600 text-xs text-center" style={{ fontFamily: 'Klados-Bold' }}>
                  📎
                </Text>
                <Text className="text-gray-500 text-xs text-center mt-1" style={{ fontFamily: 'Klados-Bold' }}>
                  Upload
                </Text>
              </TouchableOpacity>
            </View>
            
            {uploadedDocument && (
              <View className="mt-3 p-2 bg-green-50 rounded-lg border border-green-200">
                <Text className="text-green-800 text-xs" style={{ fontFamily: 'Klados-Bold' }}>
                  ✅ {uploadedDocument.name}
                </Text>
              </View>
            )}
          </View>
        ) : (
          <TextInput
            ref={inputRef}
            className="border border-gray-300 bg-gray-100 text-black rounded-lg p-4 text-base mb-4"
            value={form[currentQuestion.key as keyof typeof form]}
            onChangeText={(text) => handleChange(currentQuestion.key, text)}
            placeholder={currentQuestion.placeholder}
            placeholderTextColor="#999"
            onSubmitEditing={handleSubmitEditing}
            returnKeyType={isLastQuestion ? "done" : "next"}
            blurOnSubmit={false}
            multiline={false}
            numberOfLines={1}
          />
        )}

        {/* Navigation Buttons */}
        <View className="flex-row justify-between items-center mb-4">
          <TouchableOpacity
            className={`py-3 px-4 rounded-xl ${currentQuestionIndex === 0 ? 'opacity-50' : ''}`}
            onPress={handlePrevious}
            disabled={currentQuestionIndex === 0}
          >
            <Text className="text-gray-600 text-sm" style={{ fontFamily: 'Klados-Bold' }}>
              ← Previous
            </Text>
          </TouchableOpacity>

          <Pressable
            className={`py-3 px-6 rounded-xl ${canProceed ? 'bg-black' : 'bg-gray-400'}`}
            disabled={!canProceed}
            onPress={handleNext}
          >
            <Text className="text-white text-sm font-bold" style={{ fontFamily: 'Klados-Bold' }}>
              {isLastQuestion ? 'Generate Ideas' : 'Next →'}
            </Text>
          </Pressable>
        </View>
      </View>

      {/* Back to Dashboard Button - Fixed positioning */}
      <View className="px-6 pb-0">
        <TouchableOpacity
          className="py-4 items-center border-t border-gray-100 pt-4"
          onPress={() => {
            navigation.goBack();
          }}
        >
          <Text className="text-gray-600 text-sm underline font-medium" style={{ fontFamily: 'Klados-Bold' }}>Back to Dashboard</Text>
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}