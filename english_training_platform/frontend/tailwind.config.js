module.exports = {
          purge: ['./public/**/*.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
          darkMode: false, // or 'media' or 'class'
          theme: {
                    extend: {
                              colors: {
                                        primary: {
                                                  light: '#4DA8FF',
                                                  DEFAULT: '#0077FF',
                                                  dark: '#0055CC',
                                        },
                                        secondary: {
                                                  light: '#FFD166',
                                                  DEFAULT: '#FFC233',
                                                  dark: '#E6A800',
                                        },
                                        success: {
                                                  light: '#6DD58C',
                                                  DEFAULT: '#38C164',
                                                  dark: '#2A9D4B',
                                        },
                                        danger: {
                                                  light: '#FF6B6B',
                                                  DEFAULT: '#FF3333',
                                                  dark: '#CC0000',
                                        },
                                        neutral: {
                                                  lightest: '#FFFFFF',
                                                  lighter: '#F5F7FA',
                                                  light: '#E4E7EB',
                                                  DEFAULT: '#9AA5B1',
                                                  dark: '#616E7C',
                                                  darker: '#323F4B',
                                                  darkest: '#1F2933',
                                        },
                              },
                              fontFamily: {
                                        sans: ['Inter', 'system-ui', 'sans-serif'],
                                        serif: ['Georgia', 'serif'],
                              },
                              spacing: {
                                        '72': '18rem',
                                        '84': '21rem',
                                        '96': '24rem',
                              },
                              boxShadow: {
                                        soft: '0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03)',
                                        DEFAULT: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
                                        medium: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
                              },
                              borderRadius: {
                                        'xl': '1rem',
                                        '2xl': '1.5rem',
                              },
                    },
          },
          variants: {
                    extend: {
                              opacity: ['disabled'],
                              cursor: ['disabled'],
                              backgroundColor: ['active', 'disabled'],
                              textColor: ['active', 'disabled'],
                              borderColor: ['active', 'disabled'],
                    },
          },
          plugins: [],
} 