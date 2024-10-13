import functools

def ensure_loaded(func):
  @functools.wraps(func)
  def wrapper(self, *args, **kwargs):
      if self.vectors is None:
          raise ValueError("Vector store is not loaded. Please call load() first.")
      return func(self, *args, **kwargs)
  return wrapper
