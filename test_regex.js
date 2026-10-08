const extractFirstUrl = (text) => {
  const urlRegex = /(https?:\/\/[^\s<]+[^<.,:;"')\]\s])/;
  const match = text.match(urlRegex);
  return match ? match[0] : null;
};
console.log(extractFirstUrl("https://youtube.com/shorts/cLWe4M_GWqO?si=qmdxRQDoy9udFYNr"));
