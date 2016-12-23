//------------------------------------------------------------------------------
// <auto-generated>
//     This code was generated by a tool.
//
//     Changes to this file may cause incorrect behavior and will be lost if
//     the code is regenerated.
// </auto-generated>
//------------------------------------------------------------------------------

// Option: missing-value detection (*Specified/ShouldSerialize*/Reset*) enabled
    
// Generated from: c_table_Scene.proto
// Note: requires additional types generated from: common_degree.proto
// Note: requires additional types generated from: common_effect.proto
namespace Table
{
  [global::System.Serializable, global::ProtoBuf.ProtoContract(Name=@"Scene")]
 public partial class Scene : global::ProtoBuf.IExtensible
  {
    public Scene() {}
    

    private int? _id;
    /// <summary>
    /// ID
    /// </summary>
    [global::ProtoBuf.ProtoMember(1, IsRequired = false, Name=@"id", DataFormat = global::ProtoBuf.DataFormat.ZigZag)]
    public int id
    {
      get { return _id?? default(int); }
      set { _id = value; }
    }
    //Here has been deleted XmlIgnore
    [global::System.ComponentModel.Browsable(false)]
    public bool idSpecified
    {
      get { return _id != null; }
      set { if (value == (_id== null)) _id = value ? id : (int?)null; }
    }
    private bool ShouldSerializeid() { return idSpecified; }
    private void Resetid() { idSpecified = false; }
    

    private Common.DegreeType? _degree_type;
    /// <summary>
    /// 学位证书类别
    /// </summary>
    [global::ProtoBuf.ProtoMember(2, IsRequired = false, Name=@"degree_type", DataFormat = global::ProtoBuf.DataFormat.TwosComplement)]
    public Common.DegreeType degree_type
    {
      get { return _degree_type?? Common.DegreeType.TYPE_INVALID; }
      set { _degree_type = value; }
    }
    //Here has been deleted XmlIgnore
    [global::System.ComponentModel.Browsable(false)]
    public bool degree_typeSpecified
    {
      get { return _degree_type != null; }
      set { if (value == (_degree_type== null)) _degree_type = value ? degree_type : (Common.DegreeType?)null; }
    }
    private bool ShouldSerializedegree_type() { return degree_typeSpecified; }
    private void Resetdegree_type() { degree_typeSpecified = false; }
    
    private readonly global::System.Collections.Generic.List<uint> _ulist = new global::System.Collections.Generic.List<uint>();
    [global::ProtoBuf.ProtoMember(3, Name=@"ulist", DataFormat = global::ProtoBuf.DataFormat.TwosComplement)]
    public global::System.Collections.Generic.List<uint> ulist
    {
      get { return _ulist; }
    }
  

    private Common.Effect _effect = null;
    /// <summary>
    /// 数值效果
    /// </summary>
    [global::ProtoBuf.ProtoMember(4, IsRequired = false, Name=@"effect", DataFormat = global::ProtoBuf.DataFormat.Default)]
    [global::System.ComponentModel.DefaultValue(null)]
    public Common.Effect effect
    {
      get { return _effect; }
      set { _effect = value; }
    }
    private global::ProtoBuf.IExtension extensionObject;
    global::ProtoBuf.IExtension global::ProtoBuf.IExtensible.GetExtensionObject(bool createIfMissing)
      { return global::ProtoBuf.Extensible.GetExtensionObject(ref extensionObject, createIfMissing); }
 }
  
  [global::System.Serializable, global::ProtoBuf.ProtoContract(Name=@"Scene_ARRAY")]
  public partial class Scene_ARRAY : global::ProtoBuf.IExtensible
  {
    public Scene_ARRAY() {}
    
    private readonly global::System.Collections.Generic.List<Table.Scene> _rows = new global::System.Collections.Generic.List<Table.Scene>();
    [global::ProtoBuf.ProtoMember(1, Name=@"rows", DataFormat = global::ProtoBuf.DataFormat.Default)]
    public global::System.Collections.Generic.List<Table.Scene> rows
    {
      get { return _rows; }
    }
  
    private global::ProtoBuf.IExtension extensionObject;
    global::ProtoBuf.IExtension global::ProtoBuf.IExtensible.GetExtensionObject(bool createIfMissing)
      { return global::ProtoBuf.Extensible.GetExtensionObject(ref extensionObject, createIfMissing); }
  }
  
}