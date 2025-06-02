import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { useNavigation } from '@react-navigation/native';

// ✅ DEFINE Props ABOVE the function
type Props = {
  title: string;
  showBack?: boolean;
};

export default function CustomHeader({ title, showBack = false }: Props) {
  const navigation = useNavigation();

  return (
    <View style={styles.header}>
      {showBack ? (
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Text style={styles.backText}>← Back</Text>
        </TouchableOpacity>
      ) : (
        <View style={{ width: 50 }}>{/* placeholder for layout balance */}</View>
      )}

      <Text style={styles.title}>{title}</Text>
      <View style={{ width: 50 }}>{/* right-side filler */}</View>
    </View>
  );
}

const styles = StyleSheet.create({
  header: {
    paddingTop: 50,
    paddingBottom: 15,
    paddingHorizontal: 20,
    backgroundColor: '#fff',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderBottomWidth: 1,
    borderColor: '#eee',
  },
  title: {
    fontSize: 20,
    fontFamily: 'Inter-Bold',
    color: '#111',
    textAlign: 'center',
  },
  backText: {
    fontSize: 16,
    color: '#007AFF',
    fontFamily: 'Inter-Medium',
  },
});
