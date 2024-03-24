import * as React from 'react';

export function useLocalStorage<T>(storageKey:string, fallbackState:T) {
  const [value, setValue] = React.useState<T>(
        () => {
          const item = localStorage.getItem(storageKey);
          return item ? (JSON.parse(item) ?? fallbackState) : fallbackState;
        }
  );

  React.useEffect(() => {
    localStorage.setItem(storageKey, JSON.stringify(value));
  }, [value, storageKey]);

  return [value, setValue];
};