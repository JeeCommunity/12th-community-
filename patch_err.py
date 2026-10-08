import re
with open('src/components/PostCard.tsx', 'r') as f:
    content = f.read()

content = content.replace('''    } catch (err) {
      console.error(err);
    }
  };

  const handleReport = async (reason: string) => {''', '''    } catch (err) {
      console.error(err);
      alert('Failed to delete post.');
      setIsDeleting(false);
    }
  };

  const handleReport = async (reason: string) => {''')

content = content.replace('''    } catch (err) {
      console.error(err);
    }
  };

  const handleLike = () => {''', '''    } catch (err) {
      console.error(err);
      alert('Failed to report post.');
      setIsReporting(false);
    }
  };

  const handleLike = () => {''')

with open('src/components/PostCard.tsx', 'w') as f:
    f.write(content)
