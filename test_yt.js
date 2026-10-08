const extractYoutubeId = (url) => {
  const match = url.match(/(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/|youtube\.com\/shorts\/)([^"&?\/\s]{11})/i);
  return match ? match[1] : null;
};
console.log(extractYoutubeId("https://youtube.com/shorts/cLWe4M_GWqO?si=qmdxRQDoy9udFYNr"));
