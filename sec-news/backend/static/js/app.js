async function refreshNews() {
  try {
    const resp = await fetch('/api/refresh', {method: 'POST'});
    const data = await resp.json();
    alert(`刷新成功，新闻 ${data.news} 条，CVE ${data.cves} 条`);
    window.location.reload();
  } catch (e) {
    alert('刷新失败: ' + e);
  }
}