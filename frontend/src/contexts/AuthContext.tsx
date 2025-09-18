import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { api } from '../services/api';
import toast from 'react-hot-toast';

interface User {
  id: number;
  email?: string;
  phone_number?: string;
  first_name?: string;
  last_name?: string;
  role: string;
  is_verified: boolean;
  profile_picture?: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (emailOrPhone: string, password: string) => Promise<void>;
  loginWithOTP: (phoneNumber: string) => Promise<void>;
  verifyOTP: (phoneNumber: string, otpCode: string) => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  logout: () => void;
  updateProfile: (userData: Partial<User>) => Promise<void>;
}

interface RegisterData {
  email?: string;
  phone_number?: string;
  password: string;
  password_confirm: string;
  first_name?: string;
  last_name?: string;
  role: string;
  address?: string;
  about_me?: string;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      fetchUser();
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUser = async () => {
    try {
      const response = await api.get('/profiles/dashboard/');
      setUser(response.data);
    } catch (error) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      delete api.defaults.headers.common['Authorization'];
    } finally {
      setLoading(false);
    }
  };

  const login = async (emailOrPhone: string, password: string) => {
    try {
      const response = await api.post('/profiles/login/', {
        email_or_phone: emailOrPhone,
        password: password,
      });

      const { access, refresh, user: userData } = response.data;
      
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      api.defaults.headers.common['Authorization'] = `Bearer ${access}`;
      
      setUser(userData);
      toast.success('Login successful!');
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Login failed');
      throw error;
    }
  };

  const loginWithOTP = async (phoneNumber: string) => {
    try {
      await api.post('/profiles/otp-login/', {
        phone_number: phoneNumber,
      });
      toast.success('OTP sent to your phone number');
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to send OTP');
      throw error;
    }
  };

  const verifyOTP = async (phoneNumber: string, otpCode: string) => {
    try {
      const response = await api.post('/profiles/otp-verify/', {
        phone_number: phoneNumber,
        otp_code: otpCode,
      });

      const { access, refresh, user: userData } = response.data;
      
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      api.defaults.headers.common['Authorization'] = `Bearer ${access}`;
      
      setUser(userData);
      toast.success('OTP verified successfully!');
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Invalid OTP');
      throw error;
    }
  };

  const register = async (userData: RegisterData) => {
    try {
      await api.post('/profiles/register/', userData);
      toast.success('Registration successful! Please check your email for verification.');
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Registration failed');
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    delete api.defaults.headers.common['Authorization'];
    setUser(null);
    toast.success('Logged out successfully');
  };

  const updateProfile = async (userData: Partial<User>) => {
    try {
      const response = await api.patch('/profiles/profile-update/', userData);
      setUser(response.data);
      toast.success('Profile updated successfully');
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to update profile');
      throw error;
    }
  };

  const value: AuthContextType = {
    user,
    loading,
    login,
    loginWithOTP,
    verifyOTP,
    register,
    logout,
    updateProfile,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
