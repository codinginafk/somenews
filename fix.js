
const fs = require('fs');
const path = require('path');
const dir = 'C:/Users/DELL/OneDrive/Desktop/somenews/demo-news/src/content/news';

function setTopNews(file) {
  const p = path.join(dir, file);
  if (!fs.existsSync(p)) return;
  let text = fs.readFileSync(p, 'utf8');
  if (text.includes('trending: false')) {
    text = text.replace(/trending:\s*false/g, 'trending: true');
  } else if (!text.includes('trending: true')) {
    text = text.replace(/---\r?\n/, '---\ntrending: true\n');
  }
  
  if (text.includes('featured: false')) {
    text = text.replace(/featured:\s*false/g, 'featured: true');
  } else if (!text.includes('featured: true')) {
    text = text.replace(/---\r?\n/, '---\nfeatured: true\n');
  }
  fs.writeFileSync(p, text);
}

['nana-patekar-death-updates.md', 'cjp-protest-october-2.md', 'delhi-women-protest-rape-surge.md', 'lpu-student-perspective-demands.md', 'asian-games-2026-medal-tally-scandals-breakdown.md'].forEach(setTopNews);

const agFile = path.join(dir, 'asian-games-2026-medal-tally-scandals-breakdown.md');
fs.writeFileSync(agFile, fs.readFileSync(agFile, 'utf8').replace(/category:\s*'Reality Check'/, "category: 'By the Numbers'"));

