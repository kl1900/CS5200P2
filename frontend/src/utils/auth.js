export function getUserRole() {
  const token = localStorage.getItem("jwt");
  if (!token) return null;

  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.roles || null;
  } catch (e) {
    return null;
  }
}
