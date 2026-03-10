  # Custom Assertion Methods

module TestHelpers

  def assert_array(objekt, array_size, component_type)
    ok = true
    if objekt.class != Array
      ok = false
    elsif objekt.size != array_size
      ok = false
    else
      objekt.each {|member| ok = false if member.class != component_type }
    end
    assert ok, "Expected object <#{objekt.class}> to be an Array containing #{array_size} objects of type #{component_type}"
  end


  def assert_hash(objekt, hash_size, keys, component_type)
    ok = true
    if objekt.class != Hash
      ok = false
    elsif objekt.size != hash_size
      ok = false
    elsif objekt.keys.sort != keys.sort
      ok = false
    else
      objekt.each_value {|value| ok = false if value.class != component_type }
    end
    assert ok, "Expected object <#{objekt.class}> to be a Hash containing #{hash_size} objects of type #{component_type} for the keys #{keys}"
  end


  def assert_rwb_hash(objekt, component_type)
    # Assert that <objekt> is a hash with keys [:red, :white, :blue], and that
    # the value for each of these keys is an array of objects of class <component_type>

    ok = true
    if objekt.class != Hash
      ok = false
    elsif objekt.keys.sort != [:blue, :red, :white]
      ok = false
    elsif objekt.values.find{|vv| vv.class != Array} != nil
      ok = false
    else
      objekt.values.each do |aa|
        ok = false if aa.find {|obj| obj.class != component_type} != nil
      end
    end

    assert ok, "Expected object <#{objekt.class}> to be a Hash with keys [:red, :white, :blue] and values of type Array with each element of the array of type #{component_type}"
  end


  def assert_contain_same_objects(array1, array2)
    ok = contain_same_objects(array1, array2)
    assert ok, "Expected both arrays to contain the same objects (in any order)."
  end


  # Utility Methods for Tests

  def contain_same_objects(array1, array2)
    ok = true
    if array1.size != array2.size
      ok = false
    else
      array1.each {|obj| ok = false if array2.include?(obj) == false }
    end

    return ok
  end


end


