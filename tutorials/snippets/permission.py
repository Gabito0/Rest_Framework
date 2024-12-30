from rest_framework import permissions

class isOwnerorReadyOnly(permissions.BasePermission):
  """
  Custom permission to only allow owners of an object to edit it.
  """

  def has_object_permission(self,request,view,obj):
    # Read permisions are allowed to any request,
    # so we'll get allow GET, HEAD, or OPTIONS requests.
    if request.method in permissions.SAFE_METHODS:
      return True
    
    # Write permission are only allowed to the owner of th snippet
    return obj.owner == request.user